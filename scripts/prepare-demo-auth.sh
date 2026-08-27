#!/usr/bin/env bash
set -euo pipefail

repository_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
auth_directory="${repository_root}/deploy/secrets"
auth_file="${auth_directory}/demo.htpasswd"
username="${DEMO_USERNAME:-demo}"

if [[ -z "${DEMO_PASSWORD:-}" ]]; then
  echo "Set DEMO_PASSWORD before generating demo credentials." >&2
  exit 1
fi

mkdir -p "${auth_directory}"
password_hash="$(openssl passwd -apr1 "${DEMO_PASSWORD}")"
printf '%s:%s\n' "${username}" "${password_hash}" > "${auth_file}"
chmod 600 "${auth_file}"
echo "Created ${auth_file} for user ${username}."
