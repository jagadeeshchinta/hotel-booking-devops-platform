from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models import ReservationStatus, RoomType


class RoomBase(BaseModel):
    room_number: str = Field(..., examples=["101"])
    room_type: RoomType = Field(..., examples=[RoomType.DELUXE])
    price_per_night: Decimal = Field(..., ge=0, examples=[Decimal("150.00")])


class RoomResponse(RoomBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ReservationCreate(BaseModel):
    room_id: int = Field(..., gt=0, examples=[1], description="Target room ID")
    guest_name: str = Field(..., min_length=2, max_length=255, examples=["Sarah Connor"])
    check_in: date = Field(..., examples=["2026-12-01"], description="Check-in date (inclusive)")
    check_out: date = Field(..., examples=["2026-12-05"], description="Check-out date (exclusive)")

    @field_validator("check_out")
    @classmethod
    def validate_dates(cls, v: date, info) -> date:
        check_in = info.data.get("check_in")
        if check_in is not None and v <= check_in:
            raise ValueError(f"check_out ({v}) must be strictly after check_in ({check_in})")
        return v


class ReservationResponse(BaseModel):
    id: int
    booking_reference: str
    room_id: int
    guest_name: str
    check_in: date
    check_out: date
    status: ReservationStatus
    created_at: datetime
    room: RoomResponse | None = None

    model_config = ConfigDict(from_attributes=True)


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str


class ReadyResponse(BaseModel):
    status: str
    database: str
    detail: str | None = None


class ConflictErrorResponse(BaseModel):
    error: str
    detail: str
    room_id: int
    check_in: date
    check_out: date
