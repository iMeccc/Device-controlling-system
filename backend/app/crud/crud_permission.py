from sqlalchemy.orm import Session
from app.models.user import User
from app.models.instrument import Instrument
from app.schemas.permission import PermissionGrant # <-- Import the new schema
from . import crud_user # Import crud_user to find user by email

def grant_permission(db: Session, *, permission_in: PermissionGrant) -> User | None:
    user = db.query(User).filter(User.id == permission_in.user_id).first()
    instrument = db.query(Instrument).filter(Instrument.id == permission_in.instrument_id).first()
    
    if not user or not instrument:
        return None

    if instrument not in user.authorized_instruments:
        user.authorized_instruments.append(instrument)
        db.commit()
        db.refresh(user)
        
    return user

def revoke_permission(db: Session, *, permission_in: PermissionGrant) -> User | None:
    user = db.query(User).filter(User.id == permission_in.user_id).first()
    instrument = db.query(Instrument).filter(Instrument.id == permission_in.instrument_id).first()

    if not user or not instrument:
        return None

    if instrument in user.authorized_instruments:
        user.authorized_instruments.remove(instrument)
        db.commit()
        db.refresh(user)
        
    return user