import hashlib
import json
import os
import subprocess
from collections.abc import Mapping, Sequence
from pathlib import Path

import pytest

from app.ai.prompts import (
    FOLLOW_UP_SYSTEM_PROMPT,
    MATCHING_SYSTEM_PROMPT,
    STRUCTURED_OUTPUT_CORRECTION_PROMPT,
)
from app.ai.schemas import FollowUpResult, MatchingAnalysisResult
from app.commands.audit_release_privacy import count_prohibited_values
from app.release.smoke import (
    APPROVED_RESUME_PDF_SHA256,
    SMOKE_JOB_DESCRIPTION,
    SMOKE_QUESTION,
    ComposeRuntime,
    DatabaseCounts,
    Gateway,
    HTTPResponse,
    Runtime,
    SmokeConfig,
    SmokeFailure,
    run_smoke,
)
from evals.compose_release_artifact import compose_release_artifact
from evals.run_real_ai_evals import _schema_hash

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _prompt_hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def test_release_candidate_manifest_matches_locked_current_inputs() -> None:
    manifest = json.loads(
        (REPOSITORY_ROOT / "deploy" / "release-candidate.json").read_text(
            encoding="utf-8"
        )
    )
    evaluation = json.loads(
        (REPOSITORY_ROOT / manifest["evaluation"]["artifactPath"]).read_text(
            encoding="utf-8"
        )
    )

    assert manifest["schemaVersion"] == 1
    assert manifest["status"] == "hong_kong_production_live"
    assert manifest["provider"] == {
        "name": "ark",
        "model": "doubao-seed-2-1-pro-260628",
        "clientPath": "LangChain ChatOpenAI Responses API",
        "baseUrl": "https://ark.cn-beijing.volces.com/api/v3",
        "requestTimeoutSeconds": 180,
        "maxProviderAttempts": 2,
    }
    for dependency in manifest["dependencies"].values():
        assert _sha256(REPOSITORY_ROOT / dependency["path"]) == dependency["sha256"]
    assert _sha256(REPOSITORY_ROOT / manifest["runtimeResume"]["path"]) == (
        manifest["runtimeResume"]["sha256"]
    )
    assert _sha256(REPOSITORY_ROOT / manifest["evaluation"]["suitePath"]) == (
        manifest["evaluation"]["suiteSha256"]
    )
    assert _sha256(REPOSITORY_ROOT / manifest["evaluation"]["artifactPath"]) == (
        manifest["evaluation"]["artifactSha256"]
    )
    prerequisite = manifest["prerequisiteEvaluation"]
    assert _sha256(REPOSITORY_ROOT / prerequisite["artifactPath"]) == (
        prerequisite["artifactSha256"]
    )
    assert prerequisite["hardGuardrailsPassed"] is True
    assert manifest["evaluation"]["promptHashes"] == {
        "matching": _prompt_hash(MATCHING_SYSTEM_PROMPT),
        "followUp": _prompt_hash(FOLLOW_UP_SYSTEM_PROMPT),
        "structuredOutputCorrection": _prompt_hash(
            STRUCTURED_OUTPUT_CORRECTION_PROMPT
        ),
    }
    assert manifest["evaluation"]["schemaHashes"] == {
        "matching": _schema_hash(MatchingAnalysisResult),
        "followUp": _schema_hash(FollowUpResult),
    }
    assert manifest["evaluation"]["status"] == "passed"
    assert manifest["evaluation"]["currentCandidateValidated"] is True
    assert evaluation["hardGuardrailsPassed"] is True
    assert evaluation["runsPerCase"] == manifest["evaluation"]["runsPerCase"] == 3
    assert evaluation["providerCallsUsed"] == manifest["evaluation"]["providerCallsUsed"]
    assert evaluation["metrics"] == manifest["evaluation"]["metrics"]
    assert manifest["evaluation"]["thresholdsPassed"] is True
    assert manifest["evaluation"]["shortfalls"] == []
    assert evaluation["metrics"]["matchingStatusAccuracy"] == 1.0
    assert evaluation["metrics"]["importanceAccuracy"] == 1.0
    assert evaluation["metrics"]["followUpAnswerabilityAccuracy"] == 1.0
    assert evaluation["metrics"]["evidenceAnchorCorrectness"] == 1.0
    assert evaluation["promptHashes"] == manifest["evaluation"]["promptHashes"]
    assert evaluation["schemaHashes"] == manifest["evaluation"]["schemaHashes"]
    assert evaluation["evaluatorHash"] == manifest["evaluation"][
        "artifactEvaluatorSha256"
    ]
    assert manifest["evaluation"]["currentEvaluatorSha256"] == _sha256(
        REPOSITORY_ROOT / "backend" / "evals" / "evaluator.py"
    )
    assert manifest["evaluation"]["evaluatorEvidenceStatus"] == "passed"
    assert len(evaluation["caseRuns"]) == 45
    assert len(
        {(case_run["caseId"], case_run["runNumber"]) for case_run in evaluation["caseRuns"]}
    ) == 45
    composition = manifest["evaluation"]["composition"]
    assert composition["strategy"] == "workflow_scoped_revalidation"
    assert composition["approvedProviderCallsUsed"] == 39
    assert sum(source["includedProviderCalls"] for source in composition["sources"]) == 30
    for source in composition["sources"]:
        assert _sha256(REPOSITORY_ROOT / source["artifactPath"]) == source[
            "artifactSha256"
        ]
    assert manifest["gatewaySmoke"]["status"] == "passed"
    assert manifest["productionDeployment"] == {
        "status": "live",
        "environment": "hong_kong_production",
        "url": "https://sunnydemo.me",
        "access": "public_unauthenticated",
        "https": True,
        "certificateRenewal": "systemd_timer_with_tested_pre_post_hooks",
        "databaseBackupRestore": "passed",
        "publicAbuseControls": (
            "provider_spend_constraints_planned_application_controls_pending"
        ),
    }
    superseded = manifest["supersededEvaluation"]
    assert _sha256(REPOSITORY_ROOT / superseded["artifactPath"]) == (
        superseded["artifactSha256"]
    )
    assert superseded["thresholdsPassed"] is False


def test_final_release_artifact_is_reproducible_from_pinned_workflow_sources() -> None:
    manifest = json.loads(
        (REPOSITORY_ROOT / "deploy" / "release-candidate.json").read_text(
            encoding="utf-8"
        )
    )
    sources = manifest["evaluation"]["composition"]["sources"]
    full_source = next(source for source in sources if source["includedWorkflows"] == ["follow_up"])
    matching_source = next(
        source
        for source in sources
        if source["includedWorkflows"] == ["matching", "reliability"]
    )
    composed = compose_release_artifact(
        suite_path=REPOSITORY_ROOT / manifest["evaluation"]["suitePath"],
        full_artifact_path=REPOSITORY_ROOT / full_source["artifactPath"],
        matching_artifact_path=REPOSITORY_ROOT / matching_source["artifactPath"],
    )
    stored = json.loads(
        (REPOSITORY_ROOT / manifest["evaluation"]["artifactPath"]).read_text(
            encoding="utf-8"
        )
    )

    assert composed.model_dump(mode="json", by_alias=True, exclude={"executed_at"}) == {
        key: value for key, value in stored.items() if key != "executedAt"
    }


def test_demo_compose_is_isolated_runtime_only_and_digest_overridable() -> None:
    compose = (REPOSITORY_ROOT / "compose.demo.yaml").read_text(encoding="utf-8")
    frontend_dockerfile = (REPOSITORY_ROOT / "frontend" / "Dockerfile.demo").read_text(
        encoding="utf-8"
    )
    auth_script = (REPOSITORY_ROOT / "scripts" / "prepare-demo-auth.sh").read_text(
        encoding="utf-8"
    )
    assert compose.startswith("name: job-assistant-demo\n")
    manifest = json.loads(
        (REPOSITORY_ROOT / "deploy" / "release-candidate.json").read_text(
            encoding="utf-8"
        )
    )
    assert f"${{POSTGRES_IMAGE:-{manifest['baseImages']['database']}}}" in compose
    assert "${BACKEND_IMAGE:-job-assistant-backend:local}" in compose
    assert "${GATEWAY_IMAGE:-job-assistant-gateway:local}" in compose
    assert "${DEMO_AUTH_FILE:-./deploy/secrets/demo.htpasswd}" in compose
    backend_section = compose.split("  backend:\n", maxsplit=1)[1].split(
        "  gateway:\n", maxsplit=1
    )[0]
    gateway_section = compose.split("  gateway:\n", maxsplit=1)[1]
    assert "ARK_API_KEY:" in backend_section
    assert "ARK_API_KEY" not in gateway_section
    assert "ARK_" not in frontend_dockerfile
    assert "VITE_API_BASE_URL" in frontend_dockerfile
    assert "DEMO_AUTH_FILE:-./deploy/secrets/demo.htpasswd" in auth_script
    assert "umask 077" in auth_script
    assert "openssl passwd -6 -stdin" in auth_script
    assert "openssl passwd -apr1" not in auth_script
    backend_dockerfile = (REPOSITORY_ROOT / "backend" / "Dockerfile.demo").read_text(
        encoding="utf-8"
    )
    assert "exec .venv/bin/uvicorn" in backend_dockerfile
    assert "CMD" in backend_dockerfile
    assert "uv run" not in backend_dockerfile
    for image in manifest["baseImages"].values():
        if image == manifest["baseImages"]["database"]:
            continue
        assert image in f"{backend_dockerfile}\n{frontend_dockerfile}"
        assert "@sha256:" in image


def test_hong_kong_production_overlay_is_public_https_without_auth_mount() -> None:
    overlay = (REPOSITORY_ROOT / "compose.hk-production.yaml").read_text(
        encoding="utf-8"
    )
    nginx = (REPOSITORY_ROOT / "deploy" / "nginx.hk-production.conf").read_text(
        encoding="utf-8"
    )

    assert "FRONTEND_ORIGIN: https://sunnydemo.me" in overlay
    assert "ports: !override" in overlay
    assert '"80:80"' in overlay
    assert '"443:443"' in overlay
    assert "volumes: !override" in overlay
    assert "nginx.hk-production.conf" in overlay
    assert "demo.htpasswd" not in overlay
    assert "listen 443 ssl;" in nginx
    assert "return 301 https://$host$request_uri;" in nginx
    assert "auth_basic" not in nginx
    assert "proxy_read_timeout 400s;" in nginx


def test_demo_auth_is_sha512_and_private_on_creation(tmp_path: Path) -> None:
    auth_file = tmp_path / "demo.htpasswd"
    environment = {
        **os.environ,
        "DEMO_AUTH_FILE": str(auth_file),
        "DEMO_USERNAME": "release-reviewer",
        "DEMO_PASSWORD": "private-test-password",
    }
    completed = subprocess.run(
        ["bash", str(REPOSITORY_ROOT / "scripts" / "prepare-demo-auth.sh")],
        capture_output=True,
        text=True,
        check=False,
        env=environment,
    )

    assert completed.returncode == 0
    assert auth_file.stat().st_mode & 0o777 == 0o600
    content = auth_file.read_text(encoding="utf-8")
    assert content.startswith("release-reviewer:$6$")
    assert "private-test-password" not in content
    assert "private-test-password" not in completed.stdout
    assert "private-test-password" not in completed.stderr


def test_gateway_timeout_covers_two_finite_provider_attempts() -> None:
    manifest = json.loads(
        (REPOSITORY_ROOT / "deploy" / "release-candidate.json").read_text(
            encoding="utf-8"
        )
    )
    nginx = (REPOSITORY_ROOT / "deploy" / "nginx.demo.conf").read_text(
        encoding="utf-8"
    )
    provider_timeout = manifest["provider"]["requestTimeoutSeconds"]
    attempts = manifest["provider"]["maxProviderAttempts"]
    gateway_timeout = manifest["gateway"]["readTimeoutSeconds"]
    assert gateway_timeout >= provider_timeout * attempts + 40
    assert f"proxy_send_timeout {gateway_timeout}s;" in nginx
    assert f"proxy_read_timeout {gateway_timeout}s;" in nginx
    assert "proxy_connect_timeout 10s;" in nginx


def test_matching_prompt_keeps_independent_result_evidence_in_its_own_dimension() -> None:
    assert "定性效果必须与当前量化字段属于同一业务结果维度" in MATCHING_SYSTEM_PROMPT
    assert "不能支持收入增长字段" in MATCHING_SYSTEM_PROMPT
    assert "不得把一个独立结果字段的定性证据复用于另一个字段" in (
        MATCHING_SYSTEM_PROMPT
    )


def test_matching_prompt_requires_the_most_specific_source_heading() -> None:
    assert "最具体章节、公司、项目或岗位标题" in MATCHING_SYSTEM_PROMPT
    assert "不要改用“工作经历”等宽泛父级标题" in MATCHING_SYSTEM_PROMPT
    assert "跨标题证据必须拆成多条并各自准确定位" in MATCHING_SYSTEM_PROMPT


def test_database_privacy_scanner_detects_secret_prompt_and_raw_provider_shape() -> None:
    assert count_prohibited_values(["public markdown"], ["secret"]) == 0
    assert count_prohibited_values(["prefix secret suffix"], ["secret"]) == 1
    assert count_prohibited_values(
        [MATCHING_SYSTEM_PROMPT, '{"summary":"raw"}'],
        [MATCHING_SYSTEM_PROMPT, '"summary":'],
    ) == 2


class FakeGateway(Gateway):
    def __init__(self) -> None:
        self.matching_content = "generated-matching-private-marker"
        self.follow_up_content = "generated-follow-up-private-marker"

    def request(
        self,
        method: str,
        path: str,
        *,
        payload: Mapping[str, object] | None = None,
        authenticated: bool = True,
    ) -> HTTPResponse:
        if not authenticated:
            return HTTPResponse(401, {}, b"")
        if method == "GET" and path == "/":
            return HTTPResponse(200, {"content-type": "text/html"}, b"<html></html>")
        if method == "GET" and path == "/health":
            return _json_response(200, {"status": "ok"})
        if method == "GET" and path == "/api/resume":
            resume_path = (
                REPOSITORY_ROOT / "backend/app/resources/resume/mei_chang_resume.pdf"
            )
            body = resume_path.read_bytes()
            assert hashlib.sha256(body).hexdigest() == APPROVED_RESUME_PDF_SHA256
            return HTTPResponse(200, {"content-type": "application/pdf"}, body)
        if method == "POST" and path == "/api/matching-analysis":
            if payload == {"jobDescription": "短描述"}:
                return _json_response(
                    400, {"code": "INVALID_REQUEST", "message": "safe"}
                )
            return _json_response(
                200,
                {
                    "conversationId": "conversation_smoke",
                    "messageId": "message_matching",
                    "content": self.matching_content,
                },
            )
        if method == "POST" and path.endswith("/messages"):
            return _json_response(
                200,
                {
                    "messageId": "message_follow_up",
                    "content": self.follow_up_content,
                },
            )
        if method == "POST" and path == "/api/tracking-events":
            return _json_response(200, {"success": True})
        raise AssertionError(f"Unexpected fake request: {method} {path}")


class FakeRuntime(Runtime):
    def __init__(self, *, logs: str = "privacy-safe metadata") -> None:
        self._logs = logs
        self.cleaned = False
        self.quiesced = False

    def database_counts(
        self, _conversation_id: str, _tracking_event_id: str | None
    ) -> DatabaseCounts:
        return DatabaseCounts(0, 0, 0) if self.cleaned else DatabaseCounts(1, 4, 1)

    def run_database_counts(
        self, _run_marker: str, _tracking_event_id: str | None
    ) -> DatabaseCounts:
        return DatabaseCounts(0, 0, 0) if self.cleaned else DatabaseCounts(1, 4, 1)

    def quiesce_for_cleanup(self) -> None:
        self.quiesced = True

    def cleanup_run(self, _run_marker: str, _tracking_event_id: str | None) -> None:
        self.cleaned = True

    def logs(self) -> str:
        return self._logs

    def sensitive_values(self) -> Sequence[str]:
        return ("ark-private-marker",)

    def audit_database_privacy(self) -> None:
        return None


def _json_response(status: int, payload: Mapping[str, object]) -> HTTPResponse:
    return HTTPResponse(status, {"content-type": "application/json"}, json.dumps(payload).encode())


class RecordingComposeRuntime(ComposeRuntime):
    def __init__(self) -> None:
        super().__init__(
            compose_file=Path("compose.demo.yaml"),
            env_file=Path("deploy/demo.env"),
            project_name="job-assistant-demo",
            command_timeout_seconds=1,
        )
        self.calls: list[tuple[str, ...]] = []

    def _compose(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        self.calls.append(arguments)
        if arguments == ("logs", "--no-color"):
            stdout = "database backend gateway logs"
        elif arguments[:2] == ("exec", "-T") and arguments[2] == "backend":
            stdout = "effective-ark-secret"
        elif arguments[:2] == ("exec", "-T") and arguments[2] == "database":
            stdout = "effective-database-secret"
        else:
            raise AssertionError(f"Unexpected compose call: {arguments}")
        return subprocess.CompletedProcess(arguments, 0, stdout=stdout, stderr="")


def test_compose_privacy_uses_effective_secrets_and_all_service_logs() -> None:
    runtime = RecordingComposeRuntime()

    assert runtime.logs() == "database backend gateway logs"
    assert runtime.sensitive_values() == (
        "effective-ark-secret",
        "effective-database-secret",
    )
    assert runtime.calls[0] == ("logs", "--no-color")
    assert runtime.calls[1][2:] == (
        "backend",
        "sh",
        "-c",
        'printf %s "${ARK_API_KEY:-}"',
    )
    assert runtime.calls[2][2:] == (
        "database",
        "sh",
        "-c",
        'printf %s "${POSTGRES_PASSWORD:-}"',
    )


def test_smoke_emits_only_metadata_and_cleans_temporary_records() -> None:
    gateway = FakeGateway()
    runtime = FakeRuntime()
    records: list[Mapping[str, object]] = []
    config = SmokeConfig(
        base_url="https://example.invalid",
        username="demo",
        password="basic-auth-private-marker",
        timeout_seconds=430,
    )

    result = run_smoke(
        config=config,
        gateway=gateway,
        runtime=runtime,
        emit=records.append,
    )

    serialized = json.dumps(records, ensure_ascii=False)
    assert result.conversation_id == "conversation_smoke"
    assert runtime.cleaned is True
    assert runtime.quiesced is False
    for prohibited in (
        SMOKE_JOB_DESCRIPTION,
        SMOKE_QUESTION,
        gateway.matching_content,
        gateway.follow_up_content,
        config.password,
        "ark-private-marker",
    ):
        assert prohibited not in serialized
    assert records[-1] == {"check": "temporary_data_cleanup", "status": "passed"}


def test_smoke_fails_on_sensitive_logs_and_still_cleans() -> None:
    gateway = FakeGateway()
    runtime = FakeRuntime(logs=SMOKE_JOB_DESCRIPTION)
    with pytest.raises(SmokeFailure, match="Sensitive content"):
        run_smoke(
            config=SmokeConfig(
                base_url="https://example.invalid",
                username="demo",
                password="password",
                timeout_seconds=430,
            ),
            gateway=gateway,
            runtime=runtime,
            emit=lambda _record: None,
        )
    assert runtime.cleaned is True
    assert runtime.quiesced is True


class MalformedMatchingGateway(FakeGateway):
    def request(
        self,
        method: str,
        path: str,
        *,
        payload: Mapping[str, object] | None = None,
        authenticated: bool = True,
    ) -> HTTPResponse:
        if method == "POST" and path == "/api/matching-analysis" and payload != {
            "jobDescription": "短描述"
        }:
            return _json_response(
                200,
                {
                    "messageId": "message_committed_without_usable_response",
                    "content": "generated-private-marker",
                },
            )
        return super().request(
            method,
            path,
            payload=payload,
            authenticated=authenticated,
        )


def test_smoke_recovers_committed_matching_when_response_id_is_unusable() -> None:
    runtime = FakeRuntime()

    with pytest.raises(SmokeFailure, match="missing an identifier"):
        run_smoke(
            config=SmokeConfig(
                base_url="https://example.invalid",
                username="demo",
                password="password",
                timeout_seconds=430,
            ),
            gateway=MalformedMatchingGateway(),
            runtime=runtime,
            emit=lambda _record: None,
        )

    assert runtime.quiesced is True
    assert runtime.cleaned is True
