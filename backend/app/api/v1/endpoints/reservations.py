from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from typing import List, Any
from datetime import datetime

from app.crud import crud_reservation
from app.schemas.reservation import Reservation, ReservationCreate, ReservationUpdate
from app.api import deps
from app.models.reservation import ReservationStatus

# TODO: Import current_user dependency once authentication is integrated

router = APIRouter()

@router.post("/", response_model=Reservation, status_code=201)
def create_reservation(
    *,
    db: Session = Depends(deps.get_db),
    reservation_in: ReservationCreate,
    # current_user: models.User = Depends(deps.get_current_active_user), # This is the future goal
) -> Any:
    """
    Create a new reservation for the current user.
    """
    # --- TEMPORARY: Hardcode user_id=1 for testing ---
    # In the future, we will get the user from the access token.
    user_id_for_testing = 1 
    # --------------------------------------------------

    # Check if the requested timeslot is available
    is_available = crud_reservation.is_timeslot_available(
        db,
        instrument_id=reservation_in.instrument_id,
        start_time=reservation_in.start_time,
        end_time=reservation_in.end_time,
    )
    if not is_available:
        raise HTTPException(
            status_code=409,  # 409 Conflict is a good choice here
            detail="The requested timeslot is already booked.",
        )
    
    reservation = crud_reservation.create_with_owner(
        db=db, obj_in=reservation_in, user_id=user_id_for_testing
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
    Retrieve all reservations for a specific instrument.
    This can be used to display the calendar.
    """
    reservations = crud_reservation.get_multi_by_instrument(
        db, instrument_id=instrument_id, skip=skip, limit=limit
    )
    return reservations

@router.get("/my-reservations", response_model=List[Reservation])
def read_my_reservations(
    db: Session = Depends(deps.get_db),
    # current_user: models.User = Depends(deps.get_current_active_user), # Future goal
):
    """
    Retrieve all reservations for the current logged-in user.
    """
    # --- TEMPORARY: Hardcode user_id=1 for testing ---
    user_id_for_testing = 1
    # --------------------------------------------------

    reservations = crud_reservation.get_multi_by_user(db, user_id=user_id_for_testing)
    return reservations

@router.delete("/{reservation_id}", response_model=Reservation)
def cancel_reservation(
    *,
    reservation_id: int,
    db: Session = Depends(deps.get_db),
    # current_user: models.User = Depends(deps.get_current_active_user), # Future goal
):
    """
    Cancel a reservation. 
    A user should only be able to cancel their own reservation.
    """
    # --- TEMPORARY: Hardcode user_id=1 for testing ---
    user_id_for_testing = 1
    # --------------------------------------------------

    reservation = crud_reservation.get(db=db, id=reservation_id)
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    
    # --- TODO: Authorization Check ---
    # In the future, we must check if the reservation belongs to the current user.
    # if reservation.user_id != current_user.id:
    #     raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Instead of deleting, we update the status to "cancelled"
    update_schema = ReservationUpdate(status=ReservationStatus.CANCELLED)
    cancelled_reservation = crud_reservation.update(db=db, db_obj=reservation, obj_in=update_schema)
    return cancelled_reservation