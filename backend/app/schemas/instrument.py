from pydantic import BaseModel
from typing import Optional

# Import the InstrumentStatus enum from our model to ensure data consistency
from app.models.instrument import InstrumentStatus

# --- Base Schema ---
# Shared properties for an instrument.
class InstrumentBase(BaseModel):
    name: str
    model: Optional[str] = None
    location: str
    description: Optional[str] = None
    ip_address: Optional[str] = None
    mac_address: Optional[str] = None


# --- Schema for API Input (Creation) ---
# Properties to receive via API on instrument creation.
class InstrumentCreate(InstrumentBase):
    pass  # For now, it's the same as the base, but this allows for future expansion


# --- Schema for API Input (Update) ---
# Properties to receive via API on instrument update. All fields are optional.
class InstrumentUpdate(BaseModel):
    name: Optional[str] = None
    model: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    status: Optional[InstrumentStatus] = None
    ip_address: Optional[str] = None
    mac_address: Optional[str] = None


# --- Schema for API Output ---
# This is the main schema for returning instrument data to the client.
class Instrument(InstrumentBase):
    id: int
    is_active: bool
    status: InstrumentStatus

    class Config:
        # Pydantic V2 uses 'from_attributes' to enable ORM model mapping
        from_attributes = True