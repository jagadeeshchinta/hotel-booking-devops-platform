# 🏨 Hotel Room Availability & Reservation Service

Production-grade, minimal Hotel Room Availability and Reservation microservice built with **FastAPI**, **SQLAlchemy 2.0**, **PostgreSQL 16**, **Psycopg2**, **Nginx HTTPS Reverse Proxy**, and **Docker Compose**.

[![CI/CD Pipeline](https://img.shields.io/badge/CI%2FCD-GitHub_Actions-blue?logo=githubactions)](.github/workflows/ci-cd.yml)
[![Docker](https://img.shields.io/badge/Docker-Multi--Stage_Non--Root-2496ED?logo=docker)](Dockerfile)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16_Alpine_(GiST)-336791?logo=postgresql)](app/models.py)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?logo=fastapi)](app/main.py)
[![Security](https://img.shields.io/badge/Security-Trivy_Scanned-green?logo=aquasec)](.github/workflows/ci-cd.yml)

---

## 📑 Table of Contents

- [Architectural Overview & Highlights](#-architectural-overview--highlights)
- [Port Map & Network Matrix](#-port-map--network-matrix)
- [Environment Configuration Variables](#-environment-configuration-variables)
- [Quick Start Guide](#-quick-start-guide)
- [API Verification & cURL Examples](#-api-verification--curl-examples)
- [Automated Testing & Concurrency Invariant](#-automated-testing--concurrency-invariant)
- [Database Backup & Recovery](#-database-backup--recovery)
- [CI/CD Pipeline & GHCR Publishing](#-cicd-pipeline--ghcr-publishing)
- [Known Limitations & Assumptions](#-known-limitations--assumptions)
- [AI & Open-Source Attribution](#-ai--open-source-attribution)

---

## 🚀 Architectural Overview & Highlights

Detailed diagrams and operational procedures are documented in:
- 🏗️ **[System & CI/CD Architecture Guide](docs/architecture.md)**
- 📖 **[On-Call DevOps Operations Runbook](RUNBOOK.md)**

### Key Features
1. **Bulletproof Concurrency Control:**
   - **PostgreSQL GiST Exclusion Constraint:** Uses `btree_gist` extension to enforce:
     ```sql
     ALTER TABLE reservations
     ADD CONSTRAINT exclude_overlapping_confirmed_reservations
     EXCLUDE USING gist (
         room_id WITH =,
         daterange(check_in, check_out, '[)') WITH &&
     ) WHERE (status = 'CONFIRMED');
     ```
   - **Pessimistic Row Locking (`SELECT ... FOR UPDATE`):** Locks target room records during reservation requests, serializing concurrent booking transactions for that room.
   - **Zero Race Conditions:** Physical exclusion constraint at the database storage engine layer guarantees overlapping reservations cannot be committed, even under massive multi-threaded load.
   - **Clean Conflict Interception:** Gracefully intercepts `IntegrityError` / exclusion collisions and returns a clear `409 Conflict` JSON error with room and date details.
2. **Network Isolation & Security Hardening:**
   - Multi-stage Docker build producing a minimal runtime image based on `python:3.12-slim`.
   - Dedicated non-root user `appuser:appgroup` (UID `10001`) with read-only root files and `tmpfs: /tmp`.
   - Complete network isolation: `hotel-booking-nginx` is the **only** service with host-published ports (`80`, `443`). PostgreSQL operates on an internal-only bridge network (`backend_net`, `internal: true`) with **zero** external host exposure.
3. **Observability & Live Ops Dashboard:**
   - Liveness probe (`GET /health`) and Readiness probe (`GET /ready` executing `SELECT 1`).
   - Prometheus metrics endpoint (`GET /metrics`) exposing latency histograms and conflict/booking counters.
   - Self-contained, dark modern DevOps console page (`GET /`) for visual inspection and interactive booking.
   - Structured JSON logging (`timestamp`, `level`, `request_id`, `method`, `path`, `status_code`, `duration_ms`).

---

## 🌐 Port Map & Network Matrix

| Service | Container Name | Host Port | Container Port | Protocol | Network | External Access | Purpose |
|---|---|---|---|---|---|---|---|
| **Nginx Reverse Proxy** | `hotel-booking-nginx` | `80` | `80` | TCP (HTTP) | `frontend_net` | **Public** | Unencrypted entrypoint (301 redirect to HTTPS) |
| **Nginx Reverse Proxy** | `hotel-booking-nginx` | `443` | `443` | TCP (HTTPS) | `frontend_net` | **Public** | TLS 1.2/1.3 termination, security headers, reverse proxy |
| **FastAPI Microservice** | `hotel-booking-api` | *None* | `8000` | TCP (HTTP) | `frontend_net`, `backend_net` | **Internal Only** | REST API endpoints, metrics, live ops view |
| **PostgreSQL Database** | `hotel-booking-db` | *None* | `5432` | TCP (SQL) | `backend_net` (`internal: true`) | **Internal Only** | Relational storage with GiST exclusion constraints |

---

## ⚙️ Environment Configuration Variables

Configuration values are managed via [.env](.env) (templated in [.env.example](.env.example)):

| Variable | Default Value | Required | Description |
|---|---|---|---|
| `POSTGRES_USER` | `postgres` | Yes | Database administrative username |
| `POSTGRES_PASSWORD` | `postgres` | Yes | Database user password |
| `POSTGRES_DB` | `hotel_booking` | Yes | Target PostgreSQL database name |
| `DATABASE_URL` | `postgresql://postgres:postgres@db:5432/hotel_booking` | Yes | SQLAlchemy database connection string (points to `db` container in Compose) |
| `APP_ENV` | `production` | No | Operational environment (`development`, `testing`, `production`) |
| `LOG_LEVEL` | `INFO` | No | Application logging verbosity (`DEBUG`, `INFO`, `WARNING`, `ERROR`) |
| `IMAGE_NAME` | `hotel-booking-api` | No | Container image name (override with `ghcr.io/<org>/<repo>` for GHCR) |
| `IMAGE_TAG` | `latest` | No | Container image tag (e.g., `latest` or `sha-<short_sha>`) |

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Docker Engine 24.0+ & Docker Compose v2+
- OpenSSL (or Git for Windows / Linux / macOS)

### 2. Generate TLS Certificates
Generate self-signed SAN certificates for `localhost` and `127.0.0.1`:
```bash
# On Linux / macOS / Git Bash:
./scripts/generate-certs.sh

# On Windows PowerShell:
.\scripts\generate-certs.ps1
```

### 3. Bootstrap and Run
```bash
# Copy environment file
cp .env.example .env

# Build and start all isolated containers
docker compose up -d --build
```

### 4. Verify Active Containers
```bash
docker compose ps
```
All containers should display status `healthy` or `Up`.

---

## 📡 API Verification & cURL Examples

> **Note:** Because self-signed certificates are used locally, append `-k` (insecure) to `curl` commands.

### 1. Liveness Probe (`GET /health`)
```bash
curl -k https://localhost/health
```
```json
{"status":"healthy","service":"hotel-booking-api","version":"1.0.0"}
```

### 2. Readiness Probe (`GET /ready`)
```bash
curl -k https://localhost/ready
```
```json
{"status":"ready","database":"connected","detail":null}
```

### 3. Query Room Availability
```bash
curl -k "https://localhost/rooms/availability?check_in=2026-12-01&check_out=2026-12-05&room_type=DELUXE"
```
```json
[
  {"id":3,"room_number":"201","room_type":"DELUXE","price_per_night":"180.00"},
  {"id":4,"room_number":"202","room_type":"DELUXE","price_per_night":"210.00"}
]
```

### 4. Create a Confirmed Reservation (`POST /reservations`)
```bash
curl -k -X POST https://localhost/reservations \
  -H "Content-Type: application/json" \
  -d '{"room_id": 3, "guest_name": "Katherine Johnson", "check_in": "2026-12-01", "check_out": "2026-12-05"}'
```
```json
{
  "id": 2,
  "booking_reference": "BK-2026-4F1A9C",
  "room_id": 3,
  "guest_name": "Katherine Johnson",
  "check_in": "2026-12-01",
  "check_out": "2026-12-05",
  "status": "CONFIRMED"
}
```

### 5. Overlapping Reservation Collision (`409 Conflict`)
Submitting an overlapping check-in for the same room triggers an immediate conflict rejection:
```bash
curl -k -i -X POST https://localhost/reservations \
  -H "Content-Type: application/json" \
  -d '{"room_id": 3, "guest_name": "Overlapping Guest", "check_in": "2026-12-03", "check_out": "2026-12-08"}'
```
```text
HTTP/1.1 409 Conflict
Content-Type: application/json

{"detail":"Booking conflict: Room 201 is already booked from 2026-12-01 to 2026-12-05 (Existing reference: BK-2026-4F1A9C)."}
```

---

## 🧪 Automated Testing & Concurrency Invariant

Execute the automated test suite within the isolated environment:
```bash
docker compose run --rm api pytest tests/ -v
```

### Mandatory Concurrency Acceptance Test
Located in [tests/test_api.py](tests/test_api.py), `test_mandatory_concurrency_race_condition` launches **5 concurrent threads** via `concurrent.futures.ThreadPoolExecutor` targeting the exact same room and overlapping dates:
- **Asserts EXACTLY 1 request returns `201 Created`**.
- **Asserts EXACTLY 4 requests return `409 Conflict`**.
- Verifies database-level GiST exclusion constraint integrity.

---

## 💾 Database Backup & Recovery

Cross-platform backup and restore scripts ensure repeatable operational recovery:

### Create an On-Demand Backup
```bash
# Linux / macOS / Git Bash:
./scripts/backup.sh

# Windows PowerShell:
.\scripts\backup.ps1
```
Creates a validated SQL dump in `backups/hotel_booking_YYYYMMDD_HHMMSS.sql`.

### Restore From a Backup Dump
```bash
# Linux / macOS / Git Bash:
./scripts/restore.sh backups/hotel_booking_YYYYMMDD_HHMMSS.sql

# Windows PowerShell:
.\scripts\restore.ps1 .\backups\hotel_booking_YYYYMMDD_HHMMSS.sql
```
Restores the database schema and automatically verifies row counts for `rooms` and `reservations`.

---

## 🔄 CI/CD Pipeline & GHCR Publishing

The GitHub Actions workflow ([.github/workflows/ci-cd.yml](.github/workflows/ci-cd.yml)) executes on every push and pull request to `main`:

1. **Job 1: `lint-and-test`**
   - Spins up `postgres:16-alpine` service container with `pg_isready` health check.
   - Validates formatting and static analysis: `ruff check .` and `ruff format --check .`.
   - Runs `pytest tests/ -v` ensuring zero test failures and zero deprecation warnings.
2. **Job 2: `build-scan-and-push`**
   - Builds multi-stage Docker image with layer caching (`type=gha`).
   - Scans for vulnerabilities via **Trivy** (`aquasecurity/trivy-action@0.28.0`) at `CRITICAL,HIGH` severity levels.
   - Pushes signed, versioned image tags (`latest`, `sha-<commit>`) to GitHub Container Registry (`ghcr.io`).
   - Writes image digest and deployment evidence to `$GITHUB_STEP_SUMMARY`.

### Instant Rollback via Docker Compose
To deploy or roll back to any prior commit image:
```bash
IMAGE_NAME=ghcr.io/<org>/<repo> IMAGE_TAG=sha-<commit> docker compose up -d --no-build
```

---

## ⚠️ Known Limitations & Assumptions

1. **Self-Signed TLS Certificates:** For local evaluation and demonstration, TLS certificates are self-signed for `localhost` and `127.0.0.1`. In production deployments, these should be provisioned via automated ACME certificates (Let's Encrypt / Certbot) or a corporate PKI.
2. **Single-Node Deployment Scope:** The service is configured as a single-node Docker Compose stack. High-availability multi-region setups would require distributed PostgreSQL clustering (e.g., Patroni, AWS Aurora, or Cloud SQL) and horizontal API autoscaling behind a cloud load balancer.
3. **Authentication & Authorization:** In accordance with the project domain requirements, user authentication (OAuth2 / JWT) is deliberately omitted to keep the service minimal and focused strictly on the room availability, reservation state machine, and concurrency control domain.
4. **Timezone Standardization:** All reservation dates (`check_in`, `check_out`) are handled as UTC calendar dates (`YYYY-MM-DD`), and system timestamps default to UTC ISO-8601.

---

## 🤝 AI & Open-Source Attribution

This service was architected and implemented using modern AI-assisted engineering practices in conjunction with industry-standard open-source tools:

- **AI Tools & Assistance:**
  - Used for rapid boilerplate scaffolding, Pydantic V2 schema structuring, and test parameterization.
  - Assisted in designing the PostgreSQL GiST exclusion constraint syntax and multi-threaded `ThreadPoolExecutor` concurrency tests.
  - Assisted in generating the dark DevOps dashboard UI ([app/ui.py](app/ui.py)), Mermaid architectural diagrams, and on-call runbook procedures.
- **Open-Source Technologies & Frameworks:**
  - **[FastAPI](https://fastapi.tiangolo.com/):** High-performance Python web framework for building APIs.
  - **[SQLAlchemy 2.0](https://www.sqlalchemy.org/):** Database abstraction toolkit and ORM.
  - **[PostgreSQL 16](https://www.postgresql.org/):** Relational database engine powering `btree_gist` exclusion constraints.
  - **[Nginx 1.27 Alpine](https://nginx.org/):** High-performance reverse proxy and TLS termination gateway.
  - **[Prometheus Client](https://github.com/prometheus/client_python):** Python metrics exposition library.
  - **[Ruff](https://github.com/astral-sh/ruff):** Fast Python linter and code formatter.
  - **[Trivy](https://github.com/aquasecurity/trivy):** Vulnerability scanner for container images.
