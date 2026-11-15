#!/usr/bin/env bash
# =============================================================================
# Automated Database Restore Script (Linux / macOS / Git Bash)
# Restores a PostgreSQL .sql dump into running container and verifies row counts
# =============================================================================
set -euo pipefail

if [ $# -lt 1 ]; then
    echo "Usage: $0 <path_to_backup.sql>" >&2
    exit 1
fi

BACKUP_FILE="$1"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

if [ ! -f "${BACKUP_FILE}" ]; then
    echo "[ERROR] Backup file not found: ${BACKUP_FILE}" >&2
    exit 1
fi

CONTAINER_NAME="hotel-booking-db"
POSTGRES_USER="postgres"
POSTGRES_PASSWORD="postgres"
POSTGRES_DB="hotel_booking"

# Load credentials from .env if present
if [ -f "${ROOT_DIR}/.env" ]; then
    while IFS='=' read -r key value || [ -n "$key" ]; do
        case "$key" in
            \#*|"") continue ;;
            POSTGRES_USER) POSTGRES_USER="$value" ;;
            POSTGRES_PASSWORD) POSTGRES_PASSWORD="$value" ;;
            POSTGRES_DB) POSTGRES_DB="$value" ;;
        esac
    done < "${ROOT_DIR}/.env"
fi

echo "[INFO] Restoring '${BACKUP_FILE}' into container '${CONTAINER_NAME}' (${POSTGRES_DB})..."
cat "${BACKUP_FILE}" | docker exec -i -e PGPASSWORD="${POSTGRES_PASSWORD}" "${CONTAINER_NAME}" \
    psql -U "${POSTGRES_USER}" -d "${POSTGRES_DB}" -v ON_ERROR_STOP=1

echo "[INFO] Running recovery verification query..."
docker exec -e PGPASSWORD="${POSTGRES_PASSWORD}" "${CONTAINER_NAME}" \
    psql -U "${POSTGRES_USER}" -d "${POSTGRES_DB}" -c "
        SELECT 'rooms' AS table_name, COUNT(*) AS count FROM rooms
        UNION ALL
        SELECT 'reservations' AS table_name, COUNT(*) AS count FROM reservations;
    "

echo "[SUCCESS] Database restoration and verification completed successfully!"

