#!/bin/sh
set -eu

CERT_DIR="${CERT_DIR:-/etc/nginx/certs}"
mkdir -p "${CERT_DIR}"

if [ ! -f "${CERT_DIR}/atelier.crt" ] || [ ! -f "${CERT_DIR}/atelier.key" ]; then
  openssl req -x509 -nodes -newkey rsa:2048 -days 825 \
    -keyout "${CERT_DIR}/atelier.key" \
    -out "${CERT_DIR}/atelier.crt" \
    -subj "/CN=localhost"
fi

exec nginx -g "daemon off;"
