#!/usr/bin/env bash
set -euo pipefail

cd /opt/job-assistant-production
hook_log=/var/log/job-assistant-certbot-hook.log
docker compose \
  --env-file deploy/demo.env \
  -f compose.demo.yaml \
  -f compose.hk-production.yaml \
  up --detach --wait --no-build gateway >>"${hook_log}" 2>&1
