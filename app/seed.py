import logging
from datetime import date
from decimal import Decimal

from sqlalchemy.orm import Session

from app.models import Reservation, ReservationStatus, Room, RoomType

logger = logging.getLogger("hotel.seed")


def seed_database(db: Session) -> bool:
    """
    Idempotent database seeder.
    Checks if `rooms` is empty. If empty, populates:
      - 6 realistic rooms (2 STANDARD, 2 DELUXE, 2 SUITE)
      - 1 sample future reservation
    If already populated, safely skips without modifications.

    Returns:
        bool: True if seeded, False if skipped.
    """
    existing_rooms_count = db.query(Room).count()
    if existing_rooms_count > 0:
        logger.info(
            "Database already contains %d rooms. Skipping seed operation.",
            existing_rooms_count,
        )
        return False

    logger.info("Initializing database seed data...")

    initial_rooms = [
        Room(
            room_number="101",
            room_type=RoomType.STANDARD.value,
            price_per_night=Decimal("95.00"),
        ),
        Room(
            room_number="102",
            room_type=RoomType.STANDARD.value,
            price_per_night=Decimal("110.00"),
        ),
        Room(
            room_number="201",
            room_type=RoomType.DELUXE.value,
            price_per_night=Decimal("180.00"),
        ),
        Room(
            room_number="202",
            room_type=RoomType.DELUXE.value,
            price_per_night=Decimal("210.00"),
        ),
        Room(
            room_number="301",
            room_type=RoomType.SUITE.value,
            price_per_night=Decimal("350.00"),
        ),
        Room(
            room_number="302",
            room_type=RoomType.SUITE.value,
            price_per_night=Decimal("420.00"),
        ),
    ]

    db.add_all(initial_rooms)
    db.commit()

    # Re-query room 101 to get its assigned autoincrement ID
    room_101 = db.query(Room).filter(Room.room_number == "101").first()

    # Create 1 sample future reservation
    sample_reservation = Reservation(
        booking_reference="BK-2026-SEED01",
        room_id=room_101.id,
        guest_name="Ada Lovelace",
        check_in=date(2026, 12, 20),
        check_out=date(2026, 12, 25),
        status=ReservationStatus.CONFIRMED.value,
    )
    db.add(sample_reservation)
    db.commit()

    logger.info(
        "Successfully seeded 6 rooms and 1 future reservation (Ref: %s).",
        sample_reservation.booking_reference,
    )
    return True
