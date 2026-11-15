import concurrent.futures

import pytest
from fastapi.testclient import TestClient

from app.database import SessionLocal, init_db
from app.main import app
from app.models import Reservation, Room
from app.seed import seed_database


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """Ensure database schema, GiST extension, and seed data are ready before tests."""
    init_db()
    with SessionLocal() as db:
        db.query(Reservation).delete()
        db.query(Room).delete()
        db.commit()
        seed_database(db)
    yield


@pytest.fixture
def client():
    """Provides a fresh TestClient for each test."""
    with TestClient(app) as c:
        yield c


def test_health_probe(client: TestClient):
    """Test GET /health returns 200 with service metadata."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "hotel-booking-api"
    assert data["version"] == "1.0.0"


def test_readiness_probe(client: TestClient):
    """Test GET /ready verifies database connectivity."""
    response = client.get("/ready")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"
    assert data["database"] == "connected"


def test_metrics_endpoint(client: TestClient):
    """Test GET /metrics returns Prometheus exposition data."""
    response = client.get("/metrics")
    assert response.status_code == 200
    text_content = response.text
    assert "hotel_requests_total" in text_content
    assert "hotel_booking_conflicts_total" in text_content
    assert "hotel_bookings_confirmed_total" in text_content


def test_invalid_date_ranges_availability(client: TestClient):
    """Test GET /rooms/availability returns 400 when check_out <= check_in."""
    # check_out == check_in
    res1 = client.get("/rooms/availability?check_in=2026-10-01&check_out=2026-10-01")
    assert res1.status_code == 400
    assert "check_out" in res1.json()["detail"]

    # check_out < check_in
    res2 = client.get("/rooms/availability?check_in=2026-10-15&check_out=2026-10-10")
    assert res2.status_code == 400
    assert "check_out" in res2.json()["detail"]


def test_invalid_date_ranges_reservation(client: TestClient):
    """Test POST /reservations returns 400 or 422 when check_out <= check_in."""
    payload = {
        "room_id": 1,
        "guest_name": "Test Guest",
        "check_in": "2026-11-05",
        "check_out": "2026-11-01",
    }
    response = client.post("/reservations", json=payload)
    assert response.status_code in (400, 422)


def test_availability_filtering_before_and_after_booking(client: TestClient):
    """
    Test availability before and after a confirmed reservation:
    1. Room is initially available.
    2. Book room for target dates.
    3. Room is excluded from availability query for overlapping dates.
    4. Room remains available for non-overlapping dates.
    """
    # Find an available deluxe room
    avail_res = client.get(
        "/rooms/availability?check_in=2026-08-01&check_out=2026-08-10&room_type=DELUXE"
    )
    assert avail_res.status_code == 200
    available_rooms = avail_res.json()
    assert len(available_rooms) > 0
    target_room = available_rooms[0]
    target_room_id = target_room["id"]

    # Book target room for 2026-08-03 to 2026-08-07
    booking_payload = {
        "room_id": target_room_id,
        "guest_name": "Alan Turing",
        "check_in": "2026-08-03",
        "check_out": "2026-08-07",
    }
    book_res = client.post("/reservations", json=booking_payload)
    assert book_res.status_code == 201
    booking_data = book_res.json()
    assert booking_data["booking_reference"].startswith("BK-2026-")
    assert booking_data["status"] == "CONFIRMED"

    # Overlapping search: 2026-08-05 to 2026-08-12 (overlaps 08-03 to 08-07)
    overlap_res = client.get(
        f"/rooms/availability?check_in=2026-08-05&check_out=2026-08-12&room_type={target_room['room_type']}"
    )
    assert overlap_res.status_code == 200
    overlapping_rooms = overlap_res.json()
    assert all(r["id"] != target_room_id for r in overlapping_rooms)

    # Non-overlapping search: 2026-08-07 to 2026-08-10 (check_out is exclusive, so check_in on 08-07 is allowed)
    non_overlap_res = client.get(
        f"/rooms/availability?check_in=2026-08-07&check_out=2026-08-10&room_type={target_room['room_type']}"
    )
    assert non_overlap_res.status_code == 200
    non_overlapping_rooms = non_overlap_res.json()
    assert any(r["id"] == target_room_id for r in non_overlapping_rooms)


def test_room_type_filtering(client: TestClient):
    """Test room type query filtering returns only the requested room category."""
    res_suite = client.get(
        "/rooms/availability?check_in=2026-09-01&check_out=2026-09-05&room_type=SUITE"
    )
    assert res_suite.status_code == 200
    suites = res_suite.json()
    assert len(suites) > 0
    assert all(r["room_type"] == "SUITE" for r in suites)

    res_standard = client.get(
        "/rooms/availability?check_in=2026-09-01&check_out=2026-09-05&room_type=STANDARD"
    )
    assert res_standard.status_code == 200
    standards = res_standard.json()
    assert len(standards) > 0
    assert all(r["room_type"] == "STANDARD" for r in standards)


def test_list_reservations(client: TestClient):
    """Test GET /reservations returns recent reservations with valid schema."""
    response = client.get("/reservations")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1  # At least the seed reservation exists


def test_mandatory_concurrency_race_condition():
    """
    MANDATORY CONCURRENCY ACCEPTANCE TEST:
    Launch 5 concurrent threads (concurrent.futures.ThreadPoolExecutor)
    sending simultaneous POST /reservations requests for the EXACT same room_id
    and overlapping dates.

    Assert that EXACTLY 1 returns 201 Created and EXACTLY 4 return 409 Conflict.
    """
    # Pick room 302 (Suite) for a pristine test window
    with SessionLocal() as db:
        room = db.query(Room).filter(Room.room_number == "302").first()
        assert room is not None, "Room 302 must exist in database"
        room_id = room.id
        # Reset any existing reservations for room 302 to guarantee test isolation
        db.query(Reservation).filter(Reservation.room_id == room_id).delete()
        db.commit()

    check_in_date = "2026-10-10"
    check_out_date = "2026-10-15"

    def execute_booking_request(thread_index: int):
        with TestClient(app) as thread_client:
            payload = {
                "room_id": room_id,
                "guest_name": f"Concurrency Test Guest #{thread_index}",
                "check_in": check_in_date,
                "check_out": check_out_date,
            }
            res = thread_client.post("/reservations", json=payload)
            return res.status_code, res.json()

    # Launch 5 concurrent threads
    worker_count = 5
    with concurrent.futures.ThreadPoolExecutor(max_workers=worker_count) as executor:
        futures = [executor.submit(execute_booking_request, i) for i in range(worker_count)]
        results = [f.result() for f in futures]

    status_codes = [status_code for status_code, _ in results]

    # Verify concurrency control invariants
    created_count = status_codes.count(201)
    conflict_count = status_codes.count(409)

    assert created_count == 1, (
        f"Concurrency failure! Expected exactly 1 booking to succeed (201), "
        f"but got {created_count}. Status codes: {status_codes}"
    )
    assert conflict_count == 4, (
        f"Concurrency failure! Expected exactly 4 bookings to conflict (409), "
        f"but got {conflict_count}. Status codes: {status_codes}"
    )

    # Verify that the 201 response has valid reservation reference
    successful_payload = next(data for status, data in results if status == 201)
    assert successful_payload["booking_reference"].startswith("BK-2026-")
    assert successful_payload["status"] == "CONFIRMED"

    # Verify that the 409 responses clearly state conflict
    for status, data in results:
        if status == 409:
            assert "conflict" in data["detail"].lower() or "already" in data["detail"].lower()
