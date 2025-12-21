import enum
from sqlalchemy import Column, Integer, String, Boolean, Enum
from app.db.base import Base

class InstrumentStatus(str, enum.Enum):
    """
    Enum for the status of an instrument.
    """
    AVAILABLE = "available"
    IN_USE = "in_use"
    MAINTENANCE = "maintenance"

class Instrument(Base):
    __tablename__ = "instruments"

    # Core Information
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False, comment="The common name of the instrument")
    model = Column(String, index=True, comment="The specific model of the instrument")
    location = Column(String, nullable=False, comment="The physical location of the instrument, e.g., Room A101")
    description = Column(String, comment="A detailed description of the instrument's capabilities")
    
    # Status and Control
    is_active = Column(Boolean, default=True, nullable=False, comment="Whether the instrument is available for booking in the system")
    status = Column(Enum(InstrumentStatus), nullable=False, default=InstrumentStatus.AVAILABLE, comment="The current real-time status of the instrument")
    
    # Network Identification (for client-side security)
    ip_address = Column(String, unique=True, nullable=True, comment="The static IP address of the connected computer")
    mac_address = Column(String, unique=True, nullable=True, comment="The MAC address of the connected computer for identification")