# File: backend/app/api/v1/endpoints/reservations.py (Final, Corrected Version)

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Any

# --- Corrected Imports ---
# Import the specific model 'User' and the CRUD module directly
from app.models.user import User
from app.crud import crud_reservation
# -------------------------

from app.schemas.reservation import Reservation, ReservationCreate, ReservationUpdate
from app.api import deps
from app.models.reservation import ReservationStatus

router = APIRouter()


@router.post("/", response_model=Reservation, status_code=201)
def create_reservation(
    *,
    db: Session = Depends(deps.get_db),
    reservation_in: ReservationCreate,
    current_user: User = Depends(deps.get_current_user), # <-- Use 'User' directly
) -> Any:
    """
    Create a new reservation for the current logged-in user.
    """
    is_available = crud_reservation.is_timeslot_available(
        db,
        instrument_id=reservation_in.instrument_id,
        start_time=reservation_in.start_time,
        end_time=reservation_in.end_time,
    )
    if not is_available:
        raise HTTPException(
            status_code=409,
            detail="The requested timeslot is already booked.",
        )
    
    reservation = crud_reservation.create_with_owner(
        db=db, obj_in=reservation_in, user_id=current_user.id
    )
    return reservation


@router.get("/instrument/{instrument_id}", response_model=List[Reservation])
def read_reservations_for_instrument(
    instrument_id: int,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
):
    """
    Retrieve all reservations for a specific instrument. (Public endpoint)
    """
    reservations = crud_reservation.get_multi_by_instrument(
        db, instrument_id=instrument_id, skip=skip, limit=limit
    )
    return reservations


@router.get("/my-reservations", response_model=List[Reservation])
def read_my_reservations(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user), # <-- Use 'User' directly
):
    """
    Retrieve all reservations for the current logged-in user.
    """
    reservations = crud_reservation.get_multi_by_user(
        db, user_id=current_user.id
    )
    return reservations


@router.delete("/{reservation_id}", response_model=Reservation)
def cancel_reservation(
    *,
    reservation_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user), # <-- Use 'User' directly
):
    """
    Cancel a reservation. A user can only cancel their own reservations.
    """
    reservation = crud_reservation.get(db=db, id=reservation_id)
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    
    if reservation.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    update_schema = ReservationUpdate(status=ReservationStatus.CANCELLED)
    cancelled_reservation = crud_reservation.update(
        db=db, db_obj=reservation, obj_in=update_schema
    )
    return cancelled_reservation