#!/usr/bin/env bash
set -euo pipefail

script_directory="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repository_root="$(cd "${script_directory}/../.." && pwd)"
compose_file="${repository_root}/compose.e2e.yaml"
compose_project="job-assistant-e2e"

cleanup() {
  docker compose --project-name "${compose_project}" --file "${compose_file}" down --remove-orphans >/dev/null 2>&1 || true
}
trap cleanup EXIT

docker compose --project-name "${compose_project}" --file "${compose_file}" up --detach --wait database
npx playwright test "$@"
