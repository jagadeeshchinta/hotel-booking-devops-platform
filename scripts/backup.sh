#!/usr/bin/env bash
# =============================================================================
# Automated Database Backup Script (Linux / macOS / Git Bash)
# Dumps PostgreSQL database from running container into backups/
# =============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
BACKUP_DIR="${ROOT_DIR}/backups"

mkdir -p "${BACKUP_DIR}"

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

echo "[INFO] Checking if container '${CONTAINER_NAME}' is active..."
if ! docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo "[ERROR] Database container '${CONTAINER_NAME}' is not running." >&2
    exit 1
fi

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="${BACKUP_DIR}/hotel_booking_${TIMESTAMP}.sql"

echo "[INFO] Creating database backup for '${POSTGRES_DB}'..."
docker exec -e PGPASSWORD="${POSTGRES_PASSWORD}" "${CONTAINER_NAME}" \
    pg_dump -U "${POSTGRES_USER}" -d "${POSTGRES_DB}" --clean --if-exists > "${BACKUP_FILE}"

if [ ! -s "${BACKUP_FILE}" ]; then
    echo "[ERROR] Backup failed or generated an empty file: ${BACKUP_FILE}" >&2
    rm -f "${BACKUP_FILE}"
    exit 1
fi

FILE_SIZE=$(du -h "${BACKUP_FILE}" | cut -f1)
echo "[SUCCESS] Database backup created successfully!"
echo "  File Path: ${BACKUP_FILE}"
echo "  File Size: ${FILE_SIZE}"

