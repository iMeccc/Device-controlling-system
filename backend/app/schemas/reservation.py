from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional

# Import the model enum and the schemas for related objects
from app.models.reservation import ReservationStatus
from .user import User
from .instrument import Instrument

# --- Base Schema ---
# Shared properties for a reservation.
class ReservationBase(BaseModel):
    start_time: datetime
    end_time: datetime
    instrument_id: int

    # A custom validator to ensure end_time is after start_time
    @validator("end_time")
    def end_time_must_be_after_start_time(cls, v, values):
        if "start_time" in values and v <= values["start_time"]:
            raise ValueError("End time must be after start time")
        return v


# --- Schema for API Input (Creation) ---
# Properties to receive via API on reservation creation.
class ReservationCreate(ReservationBase):
    pass


# --- Schema for API Input (Update) ---
# Properties to receive via API on reservation update (e.g., by an admin).
class ReservationUpdate(BaseModel):
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    status: Optional[ReservationStatus] = None


# --- Schema for API Output ---
# This is the main schema for returning reservation data to the client.
# It includes the related user and instrument objects for rich responses.
class Reservation(ReservationBase):
    id: int
    status: ReservationStatus
    user_id: int
    
    # --- Nested Objects ---
    # These fields will be populated from the relationship attributes
    # of the SQLAlchemy model, thanks to from_attributes=True.
    user: User
    instrument: Instrument

    class Config:
        from_attributes = True