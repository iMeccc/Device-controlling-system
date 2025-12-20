from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum

class ReservationStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    MISSED = "missed"

class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    instrument_id = Column(Integer, ForeignKey("instruments.id"))
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    status = Column(Enum(ReservationStatus), default=ReservationStatus.APPROVED)
    
    user = relationship("User", backref="reservations")
    instrument = relationship("Instrument", backref="reservations")
