from sqlalchemy.orm import Session
from typing import List

from app.models.instrument import Instrument
from app.schemas.instrument import InstrumentCreate, InstrumentUpdate

def get(db: Session, id: int) -> Instrument | None:
    """
    Get a single instrument by its ID.
    """
    return db.query(Instrument).filter(Instrument.id == id).first()

def get_multi(db: Session, *, skip: int = 0, limit: int = 100) -> List[Instrument]:
    """
    Get a list of instruments, with pagination.
    """
    return db.query(Instrument).offset(skip).limit(limit).all()

def create(db: Session, *, obj_in: InstrumentCreate) -> Instrument:
    """
    Create a new instrument in the database.
    """
    # Convert Pydantic model to a dictionary for SQLAlchemy model creation
    db_obj = Instrument(**obj_in.dict())
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update(
    db: Session, *, db_obj: Instrument, obj_in: InstrumentUpdate
) -> Instrument:
    """
    Update an existing instrument.
    """
    # Get the dictionary of the existing database object
    obj_data = db_obj.__dict__
    
    # Get the dictionary of the update data, excluding unset fields
    update_data = obj_in.dict(exclude_unset=True)
    
    for field in obj_data:
        if field in update_data:
            setattr(db_obj, field, update_data[field])
            
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def remove(db: Session, *, id: int) -> Instrument | None:
    """
    Delete an instrument from the database.
    """
    db_obj = db.query(Instrument).get(id)
    if db_obj:
        db.delete(db_obj)
        db.commit()
    return db_obj