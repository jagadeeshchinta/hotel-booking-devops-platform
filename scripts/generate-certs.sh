#!/usr/bin/env bash
# =============================================================================
# Cross-Platform TLS SAN Certificate Generator (Linux / macOS / Git Bash)
# =============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CERTS_DIR="${SCRIPT_DIR}/../certs"

mkdir -p "${CERTS_DIR}"

echo "[INFO] Generating self-signed TLS certificates for localhost and 127.0.0.1..."

# Create OpenSSL configuration for SAN (Subject Alternative Names)
cat << 'EOF' > "${CERTS_DIR}/openssl-san.cnf"
[req]
default_bits       = 2048
distinguished_name = req_distinguished_name
req_extensions     = req_ext
x509_extensions    = v3_req
prompt             = no

[req_distinguished_name]
C  = US
ST = DevOps
L  = Local
O  = HotelBooking
OU = API
CN = localhost

[req_ext]
subjectAltName = @alt_names

[v3_req]
subjectAltName = @alt_names
basicConstraints = CA:FALSE
keyUsage = nonRepudiation, digitalSignature, keyEncipherment
extendedKeyUsage = serverAuth

[alt_names]
DNS.1 = localhost
IP.1  = 127.0.0.1
EOF

openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout "${CERTS_DIR}/server.key" \
    -out "${CERTS_DIR}/server.crt" \
    -config "${CERTS_DIR}/openssl-san.cnf"

# Set secure permissions
chmod 600 "${CERTS_DIR}/server.key" || true
chmod 644 "${CERTS_DIR}/server.crt" || true
rm -f "${CERTS_DIR}/openssl-san.cnf"

echo "[SUCCESS] Self-signed SAN certificates successfully generated:"
echo "  Private Key: ${CERTS_DIR}/server.key"
echo "  Certificate: ${CERTS_DIR}/server.crt"

