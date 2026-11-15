import json
import logging
import os
import secrets
import sys
import time
import uuid
from contextlib import asynccontextmanager
from datetime import date, datetime, timezone

from fastapi import Depends, FastAPI, HTTPException, Query, Request, Response, status
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.orm import Session

from app.database import SessionLocal, get_db, init_db
from app.metrics import (
    BOOKING_CONFLICTS_TOTAL,
    BOOKINGS_CONFIRMED_TOTAL,
    REQUEST_LATENCY,
    REQUESTS_TOTAL,
    get_latest_metrics,
)
from app.models import Reservation, ReservationStatus, Room, RoomType
from app.schemas import (
    HealthResponse,
    ReadyResponse,
    ReservationCreate,
    ReservationResponse,
    RoomResponse,
)
from app.seed import seed_database
from app.ui import INDEX_HTML


# -----------------------------------------------------------------------------
# Structured JSON Logging Setup
# -----------------------------------------------------------------------------
class JSONFormatter(logging.Formatter):
    """Custom JSON formatter outputting structured logs with standardized keys."""

    def format(self, record: logging.LogRecord) -> str:
        log_payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
        }

        # Merge standard HTTP context attributes if attached to record
        for key in ["request_id", "method", "path", "status_code", "duration_ms"]:
            val = getattr(record, key, None)
            if val is not None:
                log_payload[key] = val

        if record.exc_info:
            log_payload["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_payload)


log_level = os.getenv("LOG_LEVEL", "INFO").upper()
root_logger = logging.getLogger()
root_logger.setLevel(log_level)

# Clear existing handlers to prevent duplicate output
for handler in root_logger.handlers[:]:
    root_logger.removeHandler(handler)

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(JSONFormatter())
root_logger.addHandler(stream_handler)

logger = logging.getLogger("hotel.api")


# -----------------------------------------------------------------------------
# Application Lifespan (Startup DB Extension Init + Idempotent Seed)
# -----------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Service starting up. Initializing database and extensions...")
    try:
        init_db()
        logger.info("Database schemas and GiST exclusion constraints verified.")
    except Exception as e:
        logger.error(f"Error during database initialization: {e}", exc_info=True)

    # Execute idempotent seed data population
    db = SessionLocal()
    try:
        seed_database(db)
    except Exception as e:
        logger.error(f"Error during database seeding: {e}", exc_info=True)
    finally:
        db.close()

    logger.info("Hotel Room Availability & Reservation Service initialized successfully.")
    yield
    logger.info("Service shutting down.")


app = FastAPI(
    title="Hotel Room Availability & Reservation Service",
    description="Production-grade reservation API with bulletproof concurrency control via PostgreSQL GiST exclusion constraints.",
    version="1.0.0",
    lifespan=lifespan,
)


# -----------------------------------------------------------------------------
# Request Middleware: Correlation ID, Performance Timing & JSON Logging
# -----------------------------------------------------------------------------
@app.middleware("http")
async def logging_and_metrics_middleware(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    start_time = time.perf_counter()

    try:
        response: Response = await call_next(request)
        status_code = response.status_code
    except Exception as exc:
        status_code = 500
        duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
        logger.error(
            f"Unhandled exception processing {request.method} {request.url.path}: {exc}",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "status_code": status_code,
                "duration_ms": duration_ms,
            },
            exc_info=True,
        )
        raise exc from None

    duration_seconds = time.perf_counter() - start_time
    duration_ms = round(duration_seconds * 1000, 2)

    # Attach correlation id to response headers
    response.headers["X-Request-ID"] = request_id

    # Prometheus metrics recording
    endpoint_path = request.url.path
    if REQUESTS_TOTAL:
        REQUESTS_TOTAL.labels(
            method=request.method,
            endpoint=endpoint_path,
            status_code=status_code,
        ).inc()
    if REQUEST_LATENCY:
        REQUEST_LATENCY.labels(endpoint=endpoint_path).observe(duration_seconds)

    # Emit structured JSON log record
    logger.info(
        f"{request.method} {request.url.path} completed with {status_code} in {duration_ms}ms",
        extra={
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
            "status_code": status_code,
            "duration_ms": duration_ms,
        },
    )

    return response


# -----------------------------------------------------------------------------
# Core Routes
# -----------------------------------------------------------------------------
@app.get("/", response_class=HTMLResponse, tags=["Dashboard"])
def get_dashboard() -> HTMLResponse:
    """Live Ops View: Modern DevOps tester dashboard showing health, availability, and reservations."""
    return HTMLResponse(content=INDEX_HTML)


@app.get("/health", response_model=HealthResponse, tags=["Observability"])
def get_health() -> HealthResponse:
    """Liveness probe returning service metadata."""
    return HealthResponse(
        status="healthy",
        service="hotel-booking-api",
        version="1.0.0",
    )


@app.get(
    "/ready",
    response_model=ReadyResponse,
    responses={
        200: {"description": "PostgreSQL database connected and responsive"},
        503: {"description": "Database connection failed"},
    },
    tags=["Observability"],
)
def get_readiness(db: Session = Depends(get_db)):
    """Readiness probe executing SELECT 1 against PostgreSQL database."""
    try:
        db.execute(text("SELECT 1;"))
        return ReadyResponse(status="ready", database="connected")
    except (OperationalError, Exception) as exc:
        logger.error(f"Readiness check failed: {exc}")
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "unhealthy",
                "database": "disconnected",
                "detail": str(exc),
            },
        )


@app.get("/metrics", tags=["Observability"])
def get_metrics() -> Response:
    """Exposes Prometheus-compatible operational metrics."""
    data, content_type = get_latest_metrics()
    return Response(content=data, media_type=content_type)


@app.get("/rooms", response_model=list[RoomResponse], tags=["Rooms"])
def list_rooms(db: Session = Depends(get_db)) -> list[RoomResponse]:
    """Lists all configured hotel rooms."""
    return db.query(Room).order_by(Room.room_number.asc()).all()


@app.get("/rooms/availability", response_model=list[RoomResponse], tags=["Rooms"])
def get_available_rooms(
    check_in: date = Query(..., description="Check-in date (YYYY-MM-DD, inclusive)"),
    check_out: date = Query(..., description="Check-out date (YYYY-MM-DD, exclusive)"),
    room_type: RoomType | None = Query(
        None, description="Filter by room type (STANDARD, DELUXE, SUITE)"
    ),
    db: Session = Depends(get_db),
) -> list[RoomResponse]:
    """
    Finds rooms available for the requested date range with no overlapping CONFIRMED reservations.
    Enforces check_out > check_in.
    """
    if check_out <= check_in:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"check_out ({check_out}) must be strictly after check_in ({check_in})",
        )

    # Subquery: Room IDs that have an active overlapping reservation
    booked_room_ids = (
        db.query(Reservation.room_id)
        .filter(
            Reservation.status == ReservationStatus.CONFIRMED.value,
            Reservation.check_in < check_out,
            Reservation.check_out > check_in,
        )
        .subquery()
    )

    query = db.query(Room).filter(Room.id.notin_(select(booked_room_ids)))

    if room_type:
        query = query.filter(Room.room_type == room_type.value)

    return query.order_by(Room.room_number.asc()).all()


@app.post(
    "/reservations",
    response_model=ReservationResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Reservation confirmed and created"},
        400: {"description": "Invalid date range or request data"},
        404: {"description": "Room not found"},
        409: {"description": "Room is already booked for overlapping dates (Conflict)"},
    },
    tags=["Reservations"],
)
def create_reservation(
    payload: ReservationCreate,
    db: Session = Depends(get_db),
) -> ReservationResponse:
    """
    Creates a confirmed room reservation.

    Concurrency Control Strategy:
    1. Validates check_out > check_in.
    2. Opens transaction and locks the target room row with SELECT ... FOR UPDATE.
    3. Checks for existing overlapping CONFIRMED reservations.
    4. Relies on PostgreSQL EXCLUDE USING gist constraint as the ultimate race-condition barrier.
    5. Cleanly intercepts exclusion / integrity violations and returns 409 Conflict.
    """
    if payload.check_out <= payload.check_in:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"check_out ({payload.check_out}) must be strictly after check_in ({payload.check_in})",
        )

    # 1. Pessimistic lock: Lock the room row to serialize concurrent booking attempts for this room
    room = db.query(Room).filter(Room.id == payload.room_id).with_for_update().first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Room with id {payload.room_id} does not exist.",
        )

    # 2. Check for active overlapping reservations in application layer
    overlapping = (
        db.query(Reservation)
        .filter(
            Reservation.room_id == payload.room_id,
            Reservation.status == ReservationStatus.CONFIRMED.value,
            Reservation.check_in < payload.check_out,
            Reservation.check_out > payload.check_in,
        )
        .first()
    )

    if overlapping:
        if BOOKING_CONFLICTS_TOTAL:
            BOOKING_CONFLICTS_TOTAL.inc()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                f"Booking conflict: Room {room.room_number} is already booked from "
                f"{overlapping.check_in} to {overlapping.check_out} "
                f"(Existing reference: {overlapping.booking_reference})."
            ),
        )

    # Generate a unique booking reference: BK-2026-XXXXXX
    booking_reference = f"BK-2026-{secrets.token_hex(3).upper()}"

    new_reservation = Reservation(
        booking_reference=booking_reference,
        room_id=payload.room_id,
        guest_name=payload.guest_name.strip(),
        check_in=payload.check_in,
        check_out=payload.check_out,
        status=ReservationStatus.CONFIRMED.value,
    )

    # 3. Commit with database-level GiST exclusion constraint safety net
    try:
        db.add(new_reservation)
        db.commit()
        db.refresh(new_reservation)

        if BOOKINGS_CONFIRMED_TOTAL:
            BOOKINGS_CONFIRMED_TOTAL.inc()

        logger.info(
            f"Reservation {booking_reference} confirmed for Room {room.room_number} "
            f"({payload.check_in} to {payload.check_out}) by {payload.guest_name}"
        )
        return new_reservation

    except IntegrityError as exc:
        db.rollback()
        if BOOKING_CONFLICTS_TOTAL:
            BOOKING_CONFLICTS_TOTAL.inc()
        logger.warning(
            f"Integrity/Exclusion violation during booking for room {payload.room_id}: {exc}"
        )
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                f"Booking conflict: Room {room.room_number} is already reserved for overlapping dates "
                f"({payload.check_in} to {payload.check_out})."
            ),
        )


@app.get("/reservations", response_model=list[ReservationResponse], tags=["Reservations"])
def list_reservations(
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
) -> list[ReservationResponse]:
    """Lists recent room reservations ordered by creation date descending."""
    return (
        db.query(Reservation)
        .order_by(Reservation.created_at.desc(), Reservation.id.desc())
        .limit(limit)
        .all()
    )
