from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import List, Optional
from datetime import datetime
from datetime import date 

from app.models.reservation import Reservation
from app.schemas.reservation import ReservationCreate, ReservationUpdate

def get(db: Session, id: int) -> Optional[Reservation]:
    """
    Get a single reservation by its ID.
    """
    return db.query(Reservation).filter(Reservation.id == id).first()

def get_multi_by_user(
    db: Session, *, user_id: int, skip: int = 0, limit: int = 100
) -> List[Reservation]:
    """
    Get all reservations for a specific user.
    """
    return (
        db.query(Reservation)
        .filter(Reservation.user_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_multi_by_instrument(
    db: Session, *, instrument_id: int, skip: int = 0, limit: int = 100
) -> List[Reservation]:
    """
    Get all FUTURE reservations for a specific instrument.
    """
    today = date.today()
    return (
        db.query(Reservation)
        .filter(
            Reservation.instrument_id == instrument_id,
            Reservation.start_time >= today
        )
        .order_by(Reservation.start_time) # Good practice to sort them
        .offset(skip)
        .limit(limit)
        .all()
    )

def is_timeslot_available(
    db: Session, *, instrument_id: int, start_time: datetime, end_time: datetime
) -> bool:
    """
    Check if a given timeslot for an instrument is available.
    Returns True if available, False if there is a conflict.
    """
    # A timeslot is unavailable if there is any existing reservation that overlaps with it.
    # An overlap occurs if:
    # (Existing Start < New End) AND (Existing End > New Start)
    conflicting_reservation = (
        db.query(Reservation)
        .filter(
            Reservation.instrument_id == instrument_id,
            # We only care about confirmed or pending reservations
            Reservation.status.in_(["confirmed", "pending"]),
            and_(
                Reservation.start_time < end_time,
                Reservation.end_time > start_time,
            ),
        )
        .first()
    )
    return conflicting_reservation is None

def create_with_owner(
    db: Session, *, obj_in: ReservationCreate, user_id: int
) -> Reservation:
    db_obj = Reservation(**obj_in.dict(), user_id=user_id)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    
    # --- TODO: Email Notification Interface ---
    # This is the perfect place to trigger an email notification.
    # We have the user object (via db_obj.user) and reservation details.
    # Example: send_reservation_confirmation_email(user=db_obj.user, reservation=db_obj)
    
    return db_obj

def update(
    db: Session, *, db_obj: Reservation, obj_in: ReservationUpdate
) -> Reservation:
    """
    Update an existing reservation.
    """
    update_data = obj_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)
        
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def remove(db: Session, *, id: int) -> Optional[Reservation]:
    """
    Delete a reservation.
    """
    db_obj = db.query(Reservation).get(id)
    if db_obj:
        db.delete(db_obj)
        db.commit()
    return db_obj