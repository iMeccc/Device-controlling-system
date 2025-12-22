from sqlalchemy import Table, Column, Integer, ForeignKey
from app.db.base import Base

# This is an "association table" for the many-to-many relationship
# between User and Instrument. It does not need its own model class.
user_instrument_permission = Table(
    "user_instrument_permission",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("instrument_id", Integer, ForeignKey("instruments.id"), primary_key=True),
)