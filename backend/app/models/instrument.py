import enum
from sqlalchemy import Column, Integer, String, Boolean, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List, TYPE_CHECKING

from app.db.base import Base

if TYPE_CHECKING:
    from .reservation import Reservation

class InstrumentStatus(str, enum.Enum):
    AVAILABLE = "available"
    IN_USE = "in_use"
    MAINTENANCE = "maintenance"

class Instrument(Base):
    __tablename__ = "instruments"

    # Use Mapped and mapped_column for modern, type-annotated models
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True, nullable=False, comment="The common name")
    model: Mapped[str | None] = mapped_column(String, index=True, nullable=True, comment="The specific model")
    location: Mapped[str] = mapped_column(String, nullable=False, comment="The physical location")
    description: Mapped[str | None] = mapped_column(String, nullable=True, comment="Detailed capabilities")
    
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, comment="Is available for booking")
    status: Mapped[InstrumentStatus] = mapped_column(Enum(InstrumentStatus), nullable=False, default=InstrumentStatus.AVAILABLE)
    
    ip_address: Mapped[str | None] = mapped_column(String, unique=True, nullable=True, comment="Static IP address")
    mac_address: Mapped[str | None] = mapped_column(String, unique=True, nullable=True, comment="MAC address")

    # --- Relationships ---
    reservations: Mapped[List["Reservation"]] = relationship(
        "Reservation", 
        back_populates="instrument", 
        cascade="all, delete-orphan"
    )