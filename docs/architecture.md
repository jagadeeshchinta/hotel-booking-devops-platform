# 🏗️ System & CI/CD Architecture Documentation

This document details the architectural layout, network isolation boundaries, concurrency control design, and automated release pipeline for the **Hotel Room Availability & Reservation Service**.

---

## 1. Runtime & Network Isolation Architecture

The runtime architecture enforces a zero-trust network perimeter using Docker Compose bridge networks. The **Nginx reverse proxy** is the sole service with publicly published ports, shielding internal microservice components from direct public exposure.

```mermaid
flowchart TD
    subgraph PublicHost["Public Internet / Host Machine"]
        ClientBrowser["Web Browser (DevOps Dashboard)"]
        ClientAPI["API Consumer / Automated Tests"]
    end

    subgraph DockerPlatform["Docker Compose Environment"]
        subgraph FrontendNetwork["frontend_net (Bridge Network)"]
            Nginx["hotel-booking-nginx (nginx:1.27-alpine)<br/>• Port 80 (HTTP 301 Redirect to HTTPS)<br/>• Port 443 (TLS 1.2/1.3 Termination)<br/>• Security Headers: HSTS, X-Frame, X-Content-Type<br/>• Request Tracking: X-Request-ID Forwarding"]
        end

        subgraph BackendNetwork["backend_net (internal: true - Zero Host Access)"]
            API["hotel-booking-api (python:3.12-slim)<br/>• Port 8000 (Internal Only)<br/>• Non-Root: appuser (UID 10001)<br/>• Endpoints: /health, /ready, /metrics, /rooms, /reservations<br/>• Concurrency Guard: SELECT FOR UPDATE<br/>• Read-Only Root Filesystem with tmpfs /tmp"]
            
            DB["hotel-booking-db (postgres:16-alpine)<br/>• Port 5432 (Internal Only)<br/>• btree_gist Extension Enabled<br/>• EXCLUDE USING gist Constraint<br/>• Healthcheck: pg_isready"]
        end

        subgraph StorageLayer["Persistence & Recovery"]
            PGData[("Named Volume: pgdata<br/>/var/lib/postgresql/data")]
            HostBackups["Host Storage: ./backups/<br/>Automated SQL Dumps"]
        end
    end

    ClientBrowser -->|"HTTP :80 (Redirected)"| Nginx
    ClientBrowser -->|"HTTPS :443 (TLS Encrypted)"| Nginx
    ClientAPI -->|"HTTPS :443 (REST JSON)"| Nginx

    Nginx -->|"Proxy Pass: http://api:8000"| API
    API -->|"SQLAlchemy Session Pool"| DB

    DB -->|"Persistent Data Write"| PGData
    DB -.->|"pg_dump / psql restore"| HostBackups
```

### Network Isolation Boundaries & Security Controls

| Security Boundary | Component | Security Control Description |
|---|---|---|
| **Perimeter Entrypoint** | `hotel-booking-nginx` | Sole container publishing host ports (`80`, `443`). Drops cleartext HTTP via 301 redirect. Enforces modern TLS ciphers and HSTS headers. |
| **Service Tier** | `hotel-booking-api` | Exposes internal port `8000` solely to `frontend_net`. Runs as non-root user `appuser` (UID 10001). Write access restricted; volatile data uses `tmpfs: /tmp`. |
| **Database Tier** | `hotel-booking-db` | Located exclusively within `backend_net` (`internal: true`). Host has **no** port mapping or direct route to PostgreSQL port `5432`. |
| **Data Integrity** | PostgreSQL GiST | Automatic initialization of `btree_gist` extension; enforces physical exclusion constraint on `(room_id WITH =, daterange(check_in, check_out, '[)') WITH &&) WHERE (status = 'CONFIRMED')`. |

---

## 2. CI/CD & Automated Rollback Pipeline

The continuous integration and continuous deployment (CI/CD) workflow executes on GitHub Actions. It validates code quality, executes the multi-threaded concurrency test against a live PostgreSQL 16 container, performs static container vulnerability analysis, and publishes versioned images to the GitHub Container Registry (`ghcr.io`).

```mermaid
flowchart TD
    subgraph CodeCommit["Source Control (GitHub)"]
        Dev["Developer"] -->|"git push origin main"| GitPush["Push Event"]
        Dev -->|"git push feature -> PR"| GitPR["Pull Request Event"]
    end

    subgraph GHA_Job1["Job 1: lint-and-test"]
        CheckoutCode1["actions/checkout@v4"]
        SetupPython["actions/setup-python@v5 (Python 3.12, pip cache)"]
        PostgresService[("Service Container: postgres:16-alpine<br/>pg_isready healthcheck | port 5432:5432")]
        
        RuffLint["Ruff Linter (ruff check .)"]
        RuffFormat["Ruff Formatter (ruff format --check .)"]
        Pytest["Pytest Test Suite (pytest tests/ -v)<br/>• Health & Readiness Probes<br/>• Date Range Validations<br/>• 5-Thread GiST Concurrency Acceptance Invariant"]
    end

    subgraph GHA_Job2["Job 2: build-scan-and-push (needs: lint-and-test)"]
        CheckoutCode2["actions/checkout@v4"]
        Buildx["docker/setup-buildx-action@v3"]
        Meta["docker/metadata-action@v5<br/>• ghcr.io/repository:latest (main only)<br/>• ghcr.io/repository:sha-XXXXXXX<br/>• ghcr.io/repository:pr-NN"]
        LocalBuild["docker/build-push-action@v6<br/>(load: true, cache: type=gha)"]
        TrivyScan["Trivy Vulnerability Scan (aquasecurity/trivy-action@0.28.0)<br/>Severity: CRITICAL, HIGH | ignore-unfixed: true"]
        
        PublishCheck{"Event == push && ref == main?"}
        GHCRLogin["docker/login-action@v3 (ghcr.io)"]
        PushGHCR["docker/build-push-action@v6<br/>(push: true, tags: latest & sha-<commit>)"]
        StepSummary["Write Artifact Evidence to $GITHUB_STEP_SUMMARY<br/>• Repository URL<br/>• Version Tags<br/>• Immutable SHA256 Digest"]
    end

    subgraph DeploymentRollback["Production Deployment & Rollback"]
        TargetVM["Target Server / Local Docker Environment"]
        DeployLatest["Deploy Latest Release:<br/>docker compose up -d"]
        RollbackSha["Zero-Downtime Rollback to Specific Commit:<br/>IMAGE_NAME=ghcr.io/org/repo IMAGE_TAG=sha-abc1234 docker compose up -d --no-build"]
    end

    GitPush --> GHA_Job1
    GitPR --> GHA_Job1

    GHA_Job1 --> GHA_Job2

    CheckoutCode1 --> SetupPython --> RuffLint --> RuffFormat
    PostgresService -.->|"Live DB Connection"| Pytest
    RuffFormat --> Pytest

    CheckoutCode2 --> Buildx --> Meta --> LocalBuild --> TrivyScan --> PublishCheck
    PublishCheck -->|"Yes"| GHCRLogin --> PushGHCR --> StepSummary
    PublishCheck -->|"No (PR)"| PRComplete["PR Verified (Scan Passed)"]

    StepSummary -.->|"Registry Image"| TargetVM
    TargetVM --> DeployLatest
    TargetVM --> RollbackSha
```

### Pipeline Security & Invariants

1. **Least-Privilege Token Permissions:** The workflow declares only `contents: read`, `packages: write`, and `security-events: write`.
2. **Deterministic Build Caching:** Buildx uses GitHub Actions cache (`type=gha`) to prevent redundant compilation while ensuring layer determinism.
3. **Security Gate (Trivy):** Vulnerability scanning inspects Debian base layers and Python libraries prior to registry publishing.
4. **Auditability:** Every push to `main` produces an immutable registry digest (`sha256:...`) and commit tag (`sha-<short_sha>`) linked directly in the GitHub Actions step summary.

