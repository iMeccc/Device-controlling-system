from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime

class AccessLog(Base):
    __tablename__ = "access_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    instrument_id = Column(Integer, ForeignKey("instruments.id"))
    login_time = Column(DateTime, default=datetime.utcnow)
    logout_time = Column(DateTime, nullable=True)
    action_type = Column(String) # e.g., "login", "logout", "forced_logout"
    
    user = relationship("User")
    instrument = relationship("Instrument")
