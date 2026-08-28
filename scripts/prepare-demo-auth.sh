#!/usr/bin/env bash
set -euo pipefail
umask 077

repository_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
auth_file_setting="${DEMO_AUTH_FILE:-./deploy/secrets/demo.htpasswd}"
if [[ "${auth_file_setting}" = /* ]]; then
  auth_file="${auth_file_setting}"
else
  auth_file="${repository_root}/${auth_file_setting#./}"
fi
auth_directory="$(dirname "${auth_file}")"
username="${DEMO_USERNAME:-demo}"
password="${DEMO_PASSWORD:-}"
unset DEMO_PASSWORD

if [[ -z "${password}" ]]; then
  echo "Set DEMO_PASSWORD before generating demo credentials." >&2
  exit 1
fi
if [[ ! "${username}" =~ ^[A-Za-z0-9._-]{1,64}$ ]]; then
  echo "DEMO_USERNAME must contain only letters, numbers, dot, underscore, or hyphen." >&2
  exit 1
fi

mkdir -p "${auth_directory}"
password_hash="$(printf '%s' "${password}" | openssl passwd -6 -stdin)"
password=""
printf '%s:%s\n' "${username}" "${password_hash}" > "${auth_file}"
chmod 600 "${auth_file}"
echo "Created ${auth_file} for user ${username}."
