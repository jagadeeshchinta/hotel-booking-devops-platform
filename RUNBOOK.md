# 📖 On-Call DevOps Operations Runbook

**Service Name:** Hotel Room Availability & Reservation Service  
**Repository:** `hotel-booking-devops-platform`  
**Severity Levels:** P1 (Outage / DB Unreachable), P2 (Booking Degradation / High 409s), P3 (Minor Performance / Metric drift)  

---

## 1. Clean Bootstrap & Initial Deployment

Follow these steps to initialize and deploy the full stack from a clean checkout:

### Step 1.1: Clone and Configure Environment
```bash
# Clone the repository
git clone https://github.com/<org>/hotel-booking-devops-platform.git
cd hotel-booking-devops-platform

# Copy the environment configuration template
cp .env.example .env
```

Ensure `.env` matches your deployment targets:
```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=hotel_booking
DATABASE_URL=postgresql://postgres:postgres@db:5432/hotel_booking
APP_ENV=production
LOG_LEVEL=INFO
IMAGE_NAME=hotel-booking-api
IMAGE_TAG=latest
```

### Step 1.2: Generate TLS Certificates
Generate self-signed SAN certificates for `localhost` and `127.0.0.1`:
```bash
# Linux / macOS / Git Bash:
./scripts/generate-certs.sh

# Windows PowerShell:
.\scripts\generate-certs.ps1
```
*Verification:* Confirm `certs/server.crt` and `certs/server.key` exist.

### Step 1.3: Launch Stack via Docker Compose
```bash
docker compose up -d --build
```

---

## 2. Health, Readiness & Metrics Verification

Verify all service containers are healthy and reachable:

### Step 2.1: Check Container Health States
```bash
docker compose ps
```
**Expected Output:**
- `hotel-booking-db`: `Up (healthy)`, port `5432/tcp` (internal only)
- `hotel-booking-api`: `Up (healthy)`, port `8000/tcp` (internal only)
- `hotel-booking-nginx`: `Up`, ports `0.0.0.0:80->80/tcp`, `0.0.0.0:443->443/tcp`

### Step 2.2: Test HTTP to HTTPS Redirection (Port 80)
```bash
curl -I http://localhost/health
```
**Expected Response:** `HTTP/1.1 301 Moved Permanently` pointing to `Location: https://localhost/health`.

### Step 2.3: Test Liveness Probe (`GET /health`)
```bash
curl -k -s https://localhost/health
```
**Expected Response (`200 OK`):**
```json
{"status":"healthy","service":"hotel-booking-api","version":"1.0.0"}
```

### Step 2.4: Test Readiness Probe (`GET /ready`)
```bash
curl -k -s https://localhost/ready
```
**Expected Response (`200 OK`):**
```json
{"status":"ready","database":"connected","detail":null}
```

### Step 2.5: Scrape Prometheus Metrics (`GET /metrics`)
```bash
curl -k -s https://localhost/metrics | grep hotel_
```
**Key Gauges & Counters to Check:**
- `hotel_requests_total`
- `hotel_booking_conflicts_total`
- `hotel_bookings_confirmed_total`
- `hotel_request_duration_seconds`

---

## 3. Log Inspection & Troubleshooting

All requests emit structured JSON logs with performance timing and request correlation IDs (`X-Request-ID`).

### Step 3.1: View Live Application Logs
```bash
# Stream API logs formatted as JSON
docker compose logs -f api

# Filter logs by a specific correlation ID
docker compose logs api | grep "a183ace17ebbbe33d85b37898d7acbd0"
```

### Step 3.2: Common Error Scenarios & Resolution

#### Scenario A: `503 Service Unavailable` on `/ready`
- **Symptom:** `/ready` returns `{"status":"unhealthy","database":"disconnected"}`.
- **Root Cause:** PostgreSQL container is stopped, restarting, or credentials in `.env` are mismatched.
- **Remediation:**
  ```bash
  # Check database container status
  docker compose logs db --tail 50
  
  # Restart database if needed
  docker compose restart db
  
  # Verify connection using pg_isready
  docker compose exec db pg_isready -U postgres -d hotel_booking
  ```

#### Scenario B: `409 Conflict` on `POST /reservations`
- **Symptom:** Client receives `409 Conflict` with `detail: "Booking conflict: Room X is already reserved..."`.
- **Root Cause:** PostgreSQL GiST exclusion constraint prevented a double-booking race condition.
- **Remediation:** Expected business behavior. Verify `hotel_booking_conflicts_total` metric incremented. Client must select alternative dates or room.

#### Scenario C: TLS Certificate Handshake Errors
- **Symptom:** Curl reports `SSL certificate problem: self signed certificate`.
- **Root Cause:** The self-signed certificate is not in the system CA trust store.
- **Remediation:** For testing, use `curl -k` or configure application HTTP clients to trust `./certs/server.crt`. For production, replace `./certs/` with certificates signed by a trusted public CA (e.g., Let's Encrypt).

---

## 4. Failure & Recovery Drill

Simulate an unexpected database outage and verify automated self-healing.

### Step 4.1: Simulate Outage (Stop Database Container)
```bash
docker compose stop db
```

### Step 4.2: Verify Readiness Probe Fails
```bash
curl -k -i https://localhost/ready
```
**Expected Status:** `HTTP/1.1 503 Service Unavailable` with database disconnected payload.

### Step 4.3: Restore Database Container
```bash
docker compose start db
```

### Step 4.4: Confirm Self-Healing
```bash
# Wait 5 seconds for healthcheck
sleep 5
curl -k -s https://localhost/ready
```
**Expected Status:** `HTTP/1.1 200 OK` with `{"status":"ready","database":"connected"}`.

---

## 5. Database Backup & Restore Procedure

Cross-platform backup and restore scripts are located in `scripts/`.

### Step 5.1: Create an On-Demand Backup
```bash
# Linux / macOS / Git Bash:
./scripts/backup.sh

# Windows PowerShell:
.\scripts\backup.ps1
```
The script writes a validated, non-empty SQL dump to `./backups/hotel_booking_YYYYMMDD_HHMMSS.sql`.

### Step 5.2: Restore From a Backup Dump
```bash
# Linux / macOS / Git Bash:
./scripts/restore.sh backups/hotel_booking_YYYYMMDD_HHMMSS.sql

# Windows PowerShell:
.\scripts\restore.ps1 .\backups\hotel_booking_YYYYMMDD_HHMMSS.sql
```
*Verification:* The restore script automatically prints the recovered row counts:
```text
  table_name  | count 
--------------+-------
 rooms        |     6
 reservations |     3
```

---

## 6. Release & Rollback Procedure

Deploying a new image or reverting to a previous known-good commit is executed with zero downtime.

### Step 6.1: Roll Forward to a New Published Image
1. Locate the version tag from GitHub Container Registry (e.g., `sha-4a2b1c8` or `latest`).
2. Update `.env`:
   ```env
   IMAGE_NAME=ghcr.io/<org>/hotel-booking-devops-platform
   IMAGE_TAG=sha-4a2b1c8
   ```
3. Deploy the new image:
   ```bash
   docker compose pull api
   docker compose up -d --no-build
   ```

### Step 6.2: Emergency Rollback
To immediately roll back to a prior commit:
```bash
# Point to the previous working commit SHA
IMAGE_NAME=ghcr.io/<org>/hotel-booking-devops-platform IMAGE_TAG=sha-prev123 docker compose up -d --no-build

# Verify health probes
curl -k https://localhost/health
curl -k https://localhost/ready
```
No database downtime occurs during application container replacement.

