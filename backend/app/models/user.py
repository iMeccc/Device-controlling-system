from sqlalchemy import Boolean, Column, Integer, String, Enum
from app.db.base import Base
import enum

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    TEACHER = "teacher"
    STUDENT = "student"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, index=True)
    role = Column(Enum(UserRole), default=UserRole.STUDENT)
    is_active = Column(Boolean, default=True)

    # --- Relationships ---
    from sqlalchemy.orm import relationship, Mapped
    from typing import List, TYPE_CHECKING

    # This import is only for type hinting and is guarded by TYPE_CHECKING
    # to prevent circular import errors at runtime.
    if TYPE_CHECKING:
        from .reservation import Reservation  # Use a relative import

    # This user's list of reservations
    reservations: Mapped[List["Reservation"]] = relationship(
        "Reservation", 
        back_populates="user", 
        cascade="all, delete-orphan"
    )