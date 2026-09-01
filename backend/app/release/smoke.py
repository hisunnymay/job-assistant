import argparse
import base64
import hashlib
import json
import os
import re
import subprocess
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Protocol
from urllib.error import HTTPError
from urllib.parse import urljoin
from urllib.request import Request, urlopen
from uuid import uuid4

APPROVED_RESUME_PDF_SHA256 = (
    "03f5c8b961b6d13647cf365be3d36d84aecf714ecd0a0910c2c46fbc361768d1"
)
SMOKE_JOB_DESCRIPTION = (
    "我们招聘 AI 产品经理，必须具备大模型测试与评估平台的产品设计和研发落地经验，"
    "并能基于简历证据说明与岗位要求的匹配情况。"
)
SMOKE_QUESTION = "请基于简历说明候选人的大模型测试评估产品经验。"
IDENTIFIER_PATTERN = re.compile(r"^[A-Za-z0-9_-]{1,64}$")


class SmokeFailure(RuntimeError):
    """A privacy-safe release smoke failure."""


@dataclass(frozen=True)
class HTTPResponse:
    status: int
    headers: Mapping[str, str]
    body: bytes


@dataclass(frozen=True)
class DatabaseCounts:
    conversations: int
    messages: int
    tracking_events: int


@dataclass(frozen=True)
class SmokeConfig:
    base_url: str
    username: str
    password: str
    timeout_seconds: float


@dataclass(frozen=True)
class SmokeResult:
    conversation_id: str
    matching_message_id: str
    follow_up_message_id: str
    tracking_event_id: str


class Gateway(Protocol):
    def request(
        self,
        method: str,
        path: str,
        *,
        payload: Mapping[str, object] | None = None,
        authenticated: bool = True,
    ) -> HTTPResponse: ...


class Runtime(Protocol):
    def database_counts(
        self, conversation_id: str, tracking_event_id: str | None
    ) -> DatabaseCounts: ...

    def run_database_counts(
        self, run_marker: str, tracking_event_id: str | None
    ) -> DatabaseCounts: ...

    def quiesce_for_cleanup(self) -> None: ...

    def cleanup_run(self, run_marker: str, tracking_event_id: str | None) -> None: ...

    def logs(self) -> str: ...

    def sensitive_values(self) -> Sequence[str]: ...

    def audit_database_privacy(self) -> None: ...


class GatewayClient:
    def __init__(self, config: SmokeConfig) -> None:
        self._base_url = config.base_url.rstrip("/") + "/"
        self._timeout_seconds = config.timeout_seconds
        token = base64.b64encode(
            f"{config.username}:{config.password}".encode()
        ).decode("ascii")
        self._authorization = f"Basic {token}"

    def request(
        self,
        method: str,
        path: str,
        *,
        payload: Mapping[str, object] | None = None,
        authenticated: bool = True,
    ) -> HTTPResponse:
        data = None
        headers = {"Accept": "application/json"}
        if authenticated:
            headers["Authorization"] = self._authorization
        if payload is not None:
            data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            headers["Content-Type"] = "application/json"
        request = Request(
            urljoin(self._base_url, path.lstrip("/")),
            data=data,
            headers=headers,
            method=method,
        )
        try:
            with urlopen(request, timeout=self._timeout_seconds) as response:  # noqa: S310
                return HTTPResponse(
                    status=response.status,
                    headers=dict(response.headers.items()),
                    body=response.read(2_000_000),
                )
        except HTTPError as error:
            return HTTPResponse(
                status=error.code,
                headers=dict(error.headers.items()),
                body=error.read(2_000_000),
            )


class ComposeRuntime:
    def __init__(
        self,
        *,
        compose_file: Path,
        env_file: Path,
        project_name: str,
        command_timeout_seconds: float,
    ) -> None:
        self._compose_file = compose_file
        self._env_file = env_file
        self._project_name = project_name
        self._command_timeout_seconds = command_timeout_seconds

    def _compose(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        command = [
            "docker",
            "compose",
            "--project-name",
            self._project_name,
            "--env-file",
            str(self._env_file),
            "-f",
            str(self._compose_file),
            *arguments,
        ]
        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=self._command_timeout_seconds,
            check=False,
        )
        if completed.returncode != 0:
            raise SmokeFailure("Docker Compose release-validation command failed")
        return completed

    def database_counts(
        self, conversation_id: str, tracking_event_id: str | None
    ) -> DatabaseCounts:
        _validate_identifier(conversation_id)
        if tracking_event_id is not None:
            _validate_identifier(tracking_event_id)
        tracking_filter = (
            f"id = '{tracking_event_id}'" if tracking_event_id is not None else "FALSE"
        )
        query = (
            "SELECT "
            f"(SELECT count(*) FROM conversations WHERE id = '{conversation_id}'),"
            "(SELECT count(*) FROM conversation_messages "
            f"WHERE conversation_id = '{conversation_id}'),"
            f"(SELECT count(*) FROM user_behavior_events WHERE {tracking_filter});"
        )
        completed = self._compose(
            "exec",
            "-T",
            "database",
            "psql",
            "-U",
            "job_assistant",
            "-d",
            "job_assistant",
            "-At",
            "-F",
            "|",
            "-c",
            query,
        )
        fields = completed.stdout.strip().split("|")
        if len(fields) != 3:
            raise SmokeFailure("Persistence inspection returned an invalid shape")
        try:
            return DatabaseCounts(*(int(field) for field in fields))
        except ValueError as error:
            raise SmokeFailure("Persistence inspection returned invalid counts") from error

    def run_database_counts(
        self, run_marker: str, tracking_event_id: str | None
    ) -> DatabaseCounts:
        _validate_identifier(run_marker)
        if tracking_event_id is not None:
            _validate_identifier(tracking_event_id)
        tracking_filter = (
            f"id = '{tracking_event_id}'" if tracking_event_id is not None else "FALSE"
        )
        conversation_filter = (
            "SELECT conversation_id FROM conversation_messages "
            "WHERE message_type = 'job_description' "
            f"AND position('{run_marker}' in content) > 0"
        )
        query = (
            "SELECT "
            f"(SELECT count(*) FROM conversations WHERE id IN ({conversation_filter})),"
            "(SELECT count(*) FROM conversation_messages "
            f"WHERE conversation_id IN ({conversation_filter})),"
            f"(SELECT count(*) FROM user_behavior_events WHERE {tracking_filter});"
        )
        completed = self._compose(
            "exec",
            "-T",
            "database",
            "psql",
            "-U",
            "job_assistant",
            "-d",
            "job_assistant",
            "-At",
            "-F",
            "|",
            "-c",
            query,
        )
        fields = completed.stdout.strip().split("|")
        if len(fields) != 3:
            raise SmokeFailure("Run persistence inspection returned an invalid shape")
        try:
            return DatabaseCounts(*(int(field) for field in fields))
        except ValueError as error:
            raise SmokeFailure("Run persistence inspection returned invalid counts") from error

    def quiesce_for_cleanup(self) -> None:
        self._compose("stop", "backend")

    def cleanup_run(self, run_marker: str, tracking_event_id: str | None) -> None:
        _validate_identifier(run_marker)
        statements = []
        if tracking_event_id is not None:
            _validate_identifier(tracking_event_id)
            statements.append(
                f"DELETE FROM user_behavior_events WHERE id = '{tracking_event_id}';"
            )
        statements.append(
            "DELETE FROM conversations WHERE id IN ("
            "SELECT conversation_id FROM conversation_messages "
            "WHERE message_type = 'job_description' "
            f"AND position('{run_marker}' in content) > 0);"
        )
        self._compose(
            "exec",
            "-T",
            "database",
            "psql",
            "-U",
            "job_assistant",
            "-d",
            "job_assistant",
            "-v",
            "ON_ERROR_STOP=1",
            "-c",
            "".join(statements),
        )

    def logs(self) -> str:
        return self._compose("logs", "--no-color").stdout

    def sensitive_values(self) -> Sequence[str]:
        values = (
            self._service_environment_value("backend", "ARK_API_KEY"),
            self._service_environment_value("database", "POSTGRES_PASSWORD"),
        )
        return tuple(value for value in values if value)

    def _service_environment_value(self, service: str, variable: str) -> str:
        if (service, variable) not in {
            ("backend", "ARK_API_KEY"),
            ("database", "POSTGRES_PASSWORD"),
        }:
            raise SmokeFailure("Unsupported release secret lookup")
        completed = self._compose(
            "exec",
            "-T",
            service,
            "sh",
            "-c",
            f'printf %s "${{{variable}:-}}"',
        )
        return completed.stdout

    def audit_database_privacy(self) -> None:
        completed = self._compose(
            "exec",
            "-T",
            "backend",
            ".venv/bin/python",
            "-m",
            "app.commands.audit_release_privacy",
        )
        lines = [line for line in completed.stdout.splitlines() if line.strip()]
        try:
            result = json.loads(lines[-1])
        except (IndexError, json.JSONDecodeError) as error:
            raise SmokeFailure("Database privacy audit returned invalid metadata") from error
        if result.get("status") != "passed" or result.get("prohibitedValuesDetected") != 0:
            raise SmokeFailure("Database privacy audit failed")


def run_smoke(
    *,
    config: SmokeConfig,
    gateway: Gateway,
    runtime: Runtime,
    emit: Callable[[Mapping[str, object]], None],
) -> SmokeResult:
    run_marker = f"smoke_{uuid4().hex}"
    smoke_job_description = (
        f"{SMOKE_JOB_DESCRIPTION}\n发布验证标识：{run_marker}"
    )
    conversation_id: str | None = None
    tracking_event_id: str | None = None
    matching_content = ""
    follow_up_content = ""
    mutation_started = False
    completed = False
    try:
        _expect_status(gateway.request("GET", "/", authenticated=False), 401, "ui_auth")
        emit({"check": "unauthenticated_ui", "status": "passed"})
        _expect_status(
            gateway.request("GET", "/health", authenticated=False), 401, "api_auth"
        )
        emit({"check": "unauthenticated_api", "status": "passed"})
        _expect_status(gateway.request("GET", "/"), 200, "authenticated_ui")
        emit({"check": "authenticated_ui", "status": "passed"})

        health = _expect_json(gateway.request("GET", "/health"), 200, "health")
        if health != {"status": "ok"}:
            raise SmokeFailure("Protected health response contract mismatch")
        emit({"check": "protected_health", "status": "passed"})

        resume = gateway.request("GET", "/api/resume")
        _expect_status(resume, 200, "resume")
        if hashlib.sha256(resume.body).hexdigest() != APPROVED_RESUME_PDF_SHA256:
            raise SmokeFailure("Protected resume digest mismatch")
        emit({"check": "protected_resume", "status": "passed"})

        invalid = _expect_json(
            gateway.request(
                "POST", "/api/matching-analysis", payload={"jobDescription": "短描述"}
            ),
            400,
            "safe_invalid_request",
        )
        if invalid.get("code") != "INVALID_REQUEST":
            raise SmokeFailure("Safe invalid-request contract mismatch")
        emit({"check": "safe_failure", "status": "passed", "httpStatus": 400})

        mutation_started = True
        matching = _expect_json(
            gateway.request(
                "POST",
                "/api/matching-analysis",
                payload={"jobDescription": smoke_job_description},
            ),
            200,
            "matching",
        )
        conversation_id = _required_identifier(matching, "conversationId")
        matching_message_id = _required_identifier(matching, "messageId")
        matching_content = _required_content(matching)
        emit(
            {
                "check": "matching",
                "status": "passed",
                "conversationId": conversation_id,
                "messageId": matching_message_id,
            }
        )

        endpoint = f"/api/conversations/{conversation_id}/messages"
        follow_up = _expect_json(
            gateway.request("POST", endpoint, payload={"question": SMOKE_QUESTION}),
            200,
            "follow_up",
        )
        follow_up_message_id = _required_identifier(follow_up, "messageId")
        follow_up_content = _required_content(follow_up)
        emit(
            {
                "check": "follow_up",
                "status": "passed",
                "messageId": follow_up_message_id,
            }
        )

        replay = _expect_json(
            gateway.request("POST", endpoint, payload={"question": SMOKE_QUESTION}),
            200,
            "follow_up_replay",
        )
        if replay != follow_up:
            raise SmokeFailure("Completed identical follow-up was not replayed")
        emit({"check": "completed_follow_up_replay", "status": "passed"})

        tracking_event_id = f"event_{uuid4().hex}"
        session_id = f"session_{uuid4().hex}"
        tracking = _expect_json(
            gateway.request(
                "POST",
                "/api/tracking-events",
                payload={
                    "eventId": tracking_event_id,
                    "eventName": "matching_report_generated",
                    "sessionId": session_id,
                    "occurredAt": datetime.now(UTC).isoformat(),
                    "conversationId": conversation_id,
                },
            ),
            200,
            "tracking",
        )
        if tracking != {"success": True}:
            raise SmokeFailure("Tracking response contract mismatch")
        emit({"check": "tracking_persistence", "status": "passed"})

        counts = runtime.database_counts(conversation_id, tracking_event_id)
        if counts != DatabaseCounts(conversations=1, messages=4, tracking_events=1):
            raise SmokeFailure("Persistence counts do not match the public workflow")
        emit(
            {
                "check": "database_persistence",
                "status": "passed",
                "conversationCount": counts.conversations,
                "messageCount": counts.messages,
                "trackingEventCount": counts.tracking_events,
            }
        )

        logs = runtime.logs()
        sensitive_values = (
            config.password,
            SMOKE_JOB_DESCRIPTION,
            run_marker,
            SMOKE_QUESTION,
            matching_content,
            follow_up_content,
            *runtime.sensitive_values(),
        )
        if any(value and value in logs for value in sensitive_values):
            raise SmokeFailure("Sensitive content was detected in gateway/backend logs")
        emit({"check": "log_privacy", "status": "passed"})

        runtime.audit_database_privacy()
        emit({"check": "database_privacy", "status": "passed"})
        completed = True
        return SmokeResult(
            conversation_id=conversation_id,
            matching_message_id=matching_message_id,
            follow_up_message_id=follow_up_message_id,
            tracking_event_id=tracking_event_id,
        )
    finally:
        if mutation_started:
            if not completed:
                runtime.quiesce_for_cleanup()
            runtime.cleanup_run(run_marker, tracking_event_id)
            remaining = runtime.run_database_counts(run_marker, tracking_event_id)
            if remaining != DatabaseCounts(0, 0, 0):
                raise SmokeFailure("Smoke data cleanup did not remove temporary records")
            emit({"check": "temporary_data_cleanup", "status": "passed"})


def _expect_status(response: HTTPResponse, expected: int, check: str) -> None:
    if response.status != expected:
        raise SmokeFailure(f"{check} returned unexpected HTTP status")


def _expect_json(response: HTTPResponse, expected: int, check: str) -> dict[str, object]:
    _expect_status(response, expected, check)
    try:
        value = json.loads(response.body)
    except json.JSONDecodeError as error:
        raise SmokeFailure(f"{check} returned invalid JSON") from error
    if not isinstance(value, dict):
        raise SmokeFailure(f"{check} returned an invalid response shape")
    return value


def _required_identifier(value: Mapping[str, object], key: str) -> str:
    identifier = value.get(key)
    if not isinstance(identifier, str):
        raise SmokeFailure("Gateway response is missing an identifier")
    _validate_identifier(identifier)
    return identifier


def _required_content(value: Mapping[str, object]) -> str:
    content = value.get("content")
    if not isinstance(content, str) or not content:
        raise SmokeFailure("Gateway response is missing generated content")
    return content


def _validate_identifier(value: str) -> None:
    if IDENTIFIER_PATTERN.fullmatch(value) is None:
        raise SmokeFailure("Unsafe identifier returned by gateway")


def build_parser(repository_root: Path) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run the privacy-safe provider-enabled release gateway smoke."
    )
    parser.add_argument("--base-url", required=True)
    parser.add_argument(
        "--compose-file", type=Path, default=repository_root / "compose.demo.yaml"
    )
    parser.add_argument(
        "--env-file", type=Path, default=repository_root / "deploy" / "demo.env"
    )
    parser.add_argument("--project-name", default="job-assistant-demo")
    parser.add_argument("--timeout-seconds", type=float, default=430)
    return parser


def main(repository_root: Path) -> int:
    arguments = build_parser(repository_root).parse_args()
    username = os.getenv("DEMO_USERNAME", "").strip()
    password = os.getenv("DEMO_PASSWORD", "")
    if not username or not password:
        raise SystemExit("Set DEMO_USERNAME and DEMO_PASSWORD for the smoke run")
    if arguments.timeout_seconds <= 0:
        raise SystemExit("--timeout-seconds must be positive")
    config = SmokeConfig(
        base_url=arguments.base_url,
        username=username,
        password=password,
        timeout_seconds=arguments.timeout_seconds,
    )
    runtime = ComposeRuntime(
        compose_file=arguments.compose_file.resolve(),
        env_file=arguments.env_file.resolve(),
        project_name=arguments.project_name,
        command_timeout_seconds=arguments.timeout_seconds,
    )

    def emit(record: Mapping[str, object]) -> None:
        print(json.dumps(record, ensure_ascii=False, sort_keys=True))

    try:
        result = run_smoke(
            config=config,
            gateway=GatewayClient(config),
            runtime=runtime,
            emit=emit,
        )
    except Exception as error:  # noqa: BLE001
        emit({"status": "failed", "errorType": type(error).__name__})
        return 1
    emit(
        {
            "status": "passed",
            "conversationId": result.conversation_id,
            "matchingMessageId": result.matching_message_id,
            "followUpMessageId": result.follow_up_message_id,
            "trackingEventId": result.tracking_event_id,
        }
    )
    return 0
