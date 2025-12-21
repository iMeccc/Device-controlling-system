import enum
from sqlalchemy import Boolean, Column, Integer, String, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List, TYPE_CHECKING

from app.db.base import Base

if TYPE_CHECKING:
    from .reservation import Reservation

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    TEACHER = "teacher"
    STUDENT = "student"

class User(Base):
    __tablename__ = "users"

    # Use Mapped and mapped_column for modern, type-annotated models
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    full_name: Mapped[str | None] = mapped_column(String, index=True, nullable=True)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.STUDENT)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # --- Relationships ---
    reservations: Mapped[List["Reservation"]] = relationship(
        "Reservation", 
        back_populates="user", 
        cascade="all, delete-orphan"
    )