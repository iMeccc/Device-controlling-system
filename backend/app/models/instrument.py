from sqlalchemy import Column, Integer, String, Boolean
from app.db.base import Base

class Instrument(Base):
    __tablename__ = "instruments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String)
    ip_address = Column(String, nullable=True) # IP of the connected computer
    mac_address = Column(String, nullable=True) # MAC address for identification
    is_active = Column(Boolean, default=True)
    location = Column(String)
