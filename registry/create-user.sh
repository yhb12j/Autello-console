#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "Usage: $0 <username> <password>"
  exit 1
fi

USERNAME="$1"
PASSWORD="$2"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AUTH_DIR="${SCRIPT_DIR}/auth"
HTPASSWD_FILE="${AUTH_DIR}/htpasswd"

mkdir -p "${AUTH_DIR}"

if command -v htpasswd >/dev/null 2>&1; then
  htpasswd -Bbn "${USERNAME}" "${PASSWORD}" > "${HTPASSWD_FILE}"
elif command -v docker >/dev/null 2>&1; then
  docker run --rm --entrypoint htpasswd httpd:2 -Bbn "${USERNAME}" "${PASSWORD}" > "${HTPASSWD_FILE}"
else
  echo "htpasswd or Docker is required to create a registry user"
  exit 1
fi

chmod 644 "${HTPASSWD_FILE}"
echo "Registry user '${USERNAME}' written to ${HTPASSWD_FILE}"
