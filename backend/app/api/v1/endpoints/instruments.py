from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.crud import crud_instrument
from app.schemas.instrument import Instrument, InstrumentCreate, InstrumentUpdate
from app.api import deps
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=Instrument, status_code=201)
def create_instrument(
    instrument_in: InstrumentCreate,
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_active_admin),
):
    """
    Create a new instrument in the system (Admins only).
    """
    instrument = crud_instrument.create(db=db, obj_in=instrument_in)
    return instrument

@router.get("/", response_model=List[Instrument])
def read_instruments(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
):
    """
    Retrieve a list of all instruments.
    """
    instruments = crud_instrument.get_multi(db, skip=skip, limit=limit)
    return instruments

@router.get("/{instrument_id}", response_model=Instrument)
def read_instrument(
    instrument_id: int,
    db: Session = Depends(deps.get_db),
):
    """
    Get a specific instrument by its ID.
    """
    instrument = crud_instrument.get(db=db, id=instrument_id)
    if not instrument:
        raise HTTPException(status_code=404, detail="Instrument not found")
    return instrument

@router.put("/{instrument_id}", response_model=Instrument)
def update_instrument(
    instrument_id: int,
    instrument_in: InstrumentUpdate,
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_active_admin),
):
    """
    Update an existing instrument (Admins only).
    """
    instrument = crud_instrument.get(db=db, id=instrument_id)
    if not instrument:
        raise HTTPException(status_code=404, detail="Instrument not found")
    
    instrument = crud_instrument.update(db=db, db_obj=instrument, obj_in=instrument_in)
    return instrument

@router.delete("/{instrument_id}", response_model=Instrument)
def delete_instrument(
    instrument_id: int,
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_active_admin),
):
    """
    Delete an instrument from the system (Admins only).
    """
    instrument = crud_instrument.get(db=db, id=instrument_id)
    if not instrument:
        raise HTTPException(status_code=404, detail="Instrument not found")
        
    deleted_instrument = crud_instrument.remove(db=db, id=instrument_id)
    return deleted_instrument