import argparse
import json
from datetime import UTC, datetime
from pathlib import Path

from evals.evaluator import aggregate_metrics
from evals.models import CaseRunResult, EvaluationArtifact
from evals.run_real_ai_evals import _assert_artifact_privacy, load_suite, write_artifact


def compose_release_artifact(
    *,
    suite_path: Path,
    full_artifact_path: Path,
    matching_artifact_path: Path,
) -> EvaluationArtifact:
    suite, _ = load_suite(suite_path)
    full = _load_artifact(full_artifact_path)
    matching = _load_artifact(matching_artifact_path)
    _validate_compatible(full=full, matching=matching)

    full_runs = _index_runs(full.case_runs)
    matching_runs = _index_runs(matching.case_runs)
    selected: list[CaseRunResult] = []
    for run_number in range(1, full.runs_per_case + 1):
        for case in suite.cases:
            source = matching_runs if case.workflow in {"matching", "reliability"} else full_runs
            key = (case.case_id, run_number)
            try:
                selected.append(source[key])
            except KeyError as error:
                raise ValueError(
                    f"Source artifact is missing required case run: {key}"
                ) from error

    hard_guardrails_passed = all(
        rule.passed for case_run in selected for rule in case_run.rule_results
    ) and all(
        "forbidden_claim_marker_detected" not in case_run.failure_categories
        for case_run in selected
    )
    artifact = full.model_copy(
        update={
            "executed_at": datetime.now(UTC).isoformat(),
            "prompt_hashes": {
                "matching": matching.prompt_hashes["matching"],
                "followUp": full.prompt_hashes["followUp"],
                "structuredOutputCorrection": full.prompt_hashes[
                    "structuredOutputCorrection"
                ],
            },
            "provider_calls_used": sum(run.provider_calls for run in selected),
            "hard_guardrails_passed": hard_guardrails_passed,
            "metrics": aggregate_metrics(selected),
            "case_runs": selected,
        }
    )
    _assert_artifact_privacy(
        artifact,
        suite=suite,
        generated_outputs=(),
        sensitive_values=(),
    )
    return artifact


def _load_artifact(path: Path) -> EvaluationArtifact:
    return EvaluationArtifact.model_validate(
        json.loads(path.read_text(encoding="utf-8"))
    )


def _validate_compatible(
    *, full: EvaluationArtifact, matching: EvaluationArtifact
) -> None:
    if any(
        (
            full.suite_id != matching.suite_id,
            full.suite_hash != matching.suite_hash,
            full.model != matching.model,
            full.client_path != matching.client_path,
            full.runs_per_case != matching.runs_per_case,
            full.evaluator_hash != matching.evaluator_hash,
            full.schema_hashes != matching.schema_hashes,
            full.prompt_hashes["followUp"] != matching.prompt_hashes["followUp"],
            full.prompt_hashes["structuredOutputCorrection"]
            != matching.prompt_hashes["structuredOutputCorrection"],
        )
    ):
        raise ValueError("Evaluation artifacts are not composition-compatible")


def _index_runs(case_runs: list[CaseRunResult]) -> dict[tuple[str, int], CaseRunResult]:
    indexed = {(case_run.case_id, case_run.run_number): case_run for case_run in case_runs}
    if len(indexed) != len(case_runs):
        raise ValueError("Evaluation artifact contains duplicate case runs")
    return indexed


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compose a complete release artifact from workflow-scoped reruns"
    )
    parser.add_argument("--cases", required=True, type=Path)
    parser.add_argument("--full-artifact", required=True, type=Path)
    parser.add_argument("--matching-artifact", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    artifact = compose_release_artifact(
        suite_path=args.cases,
        full_artifact_path=args.full_artifact,
        matching_artifact_path=args.matching_artifact,
    )
    write_artifact(args.output, artifact)


if __name__ == "__main__":
    main()
