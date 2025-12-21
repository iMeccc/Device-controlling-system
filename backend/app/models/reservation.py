import enum
from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.db.base import Base
from typing import TYPE_CHECKING

# These imports are only for type hinting and are guarded by TYPE_CHECKING
if TYPE_CHECKING:
    from .user import User
    from .instrument import Instrument

class ReservationStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"  # Changed from APPROVED for clarity
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    MISSED = "missed"

class Reservation(Base):
    __tablename__ = "reservations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    start_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    status: Mapped[ReservationStatus] = mapped_column(Enum(ReservationStatus), nullable=False, default=ReservationStatus.CONFIRMED)
    
    # --- Foreign Keys ---
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    instrument_id: Mapped[int] = mapped_column(Integer, ForeignKey("instruments.id"))

    # --- Relationships ---
    # The 'user' who made this reservation
    user: Mapped["User"] = relationship("User", back_populates="reservations")
    # The 'instrument' being reserved
    instrument: Mapped["Instrument"] = relationship("Instrument", back_populates="reservations")