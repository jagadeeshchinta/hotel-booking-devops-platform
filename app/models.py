import enum

from sqlalchemy import (
    Column,
    Date,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    column,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import ExcludeConstraint
from sqlalchemy.orm import relationship

from app.database import Base


class RoomType(str, enum.Enum):
    STANDARD = "STANDARD"
    DELUXE = "DELUXE"
    SUITE = "SUITE"


class ReservationStatus(str, enum.Enum):
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    room_number = Column(String(50), unique=True, nullable=False, index=True)
    room_type = Column(String(20), nullable=False, index=True)
    price_per_night = Column(Numeric(10, 2), nullable=False)

    reservations = relationship(
        "Reservation",
        back_populates="room",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Room(id={self.id}, number={self.room_number}, type={self.room_type})>"


class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    booking_reference = Column(String(64), unique=True, nullable=False, index=True)
    room_id = Column(
        Integer,
        ForeignKey("rooms.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    guest_name = Column(String(255), nullable=False)
    check_in = Column(Date, nullable=False, index=True)
    check_out = Column(Date, nullable=False, index=True)
    status = Column(
        String(20),
        nullable=False,
        default=ReservationStatus.CONFIRMED.value,
        server_default=text("'CONFIRMED'"),
        index=True,
    )
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    room = relationship("Room", back_populates="reservations")

    __table_args__ = (
        ExcludeConstraint(
            (column("room_id"), "="),
            (func.daterange(column("check_in"), column("check_out"), "[)"), "&&"),
            where=(column("status") == "CONFIRMED"),
            name="exclude_overlapping_confirmed_reservations",
            using="gist",
        ),
        Index("ix_reservations_room_active_dates", "room_id", "status", "check_in", "check_out"),
    )

    def __repr__(self) -> str:
        return (
            f"<Reservation(ref={self.booking_reference}, room_id={self.room_id}, "
            f"guest={self.guest_name}, dates={self.check_in} to {self.check_out})>"
        )
