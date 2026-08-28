import argparse
import json
from pathlib import Path

from evals.evaluator import rescore_artifact
from evals.models import EvaluationArtifact
from evals.run_real_ai_evals import (
    _assert_artifact_privacy,
    _sha256_bytes,
    load_suite,
    write_artifact,
)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Re-score an existing privacy-safe Goal 8 artifact without provider calls"
    )
    parser.add_argument("--cases", required=True, type=Path)
    parser.add_argument("--artifact", required=True, type=Path)
    args = parser.parse_args()

    suite, suite_bytes = load_suite(args.cases)
    artifact = EvaluationArtifact.model_validate(
        json.loads(args.artifact.read_text(encoding="utf-8"))
    )
    if artifact.suite_hash != _sha256_bytes(suite_bytes):
        raise SystemExit("Artifact suite hash does not match the supplied case file")
    rescored = rescore_artifact(artifact, suite=suite)
    _assert_artifact_privacy(
        rescored,
        suite=suite,
        generated_outputs=(),
        sensitive_values=(),
    )
    write_artifact(args.artifact, rescored)


if __name__ == "__main__":
    main()
