#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 '<ssh-public-key>'"
  exit 1
fi

KEY="$1"
SSH_DIR="${HOME}/.ssh"
AUTH_FILE="${SSH_DIR}/authorized_keys"

mkdir -p "${SSH_DIR}"
chmod 700 "${SSH_DIR}"
touch "${AUTH_FILE}"
chmod 600 "${AUTH_FILE}"

if grep -qxF "${KEY}" "${AUTH_FILE}"; then
  echo "Key is already present in ${AUTH_FILE}"
else
  printf '%s\n' "${KEY}" >> "${AUTH_FILE}"
  echo "Key added to ${AUTH_FILE}"
fi
