from datetime import datetime
from sqlalchemy import Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import TYPE_CHECKING, Optional, List # <-- 1. Import 'Optional' and 'List'

from app.db.base import Base

if TYPE_CHECKING:
    from .user import User

class AccessLog(Base):
    __tablename__ = "access_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    
    user_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    action: Mapped[str] = mapped_column(String, index=True, nullable=False)
    
    # --- FIX: Use Optional[dict] for better compatibility ---
    details: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    # --- Relationship ---
    user: Mapped[Optional["User"]] = relationship("User", back_populates="logs")