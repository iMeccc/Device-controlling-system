from sqlalchemy.orm import Session
from typing import Optional, cast

from app.core.security import get_password_hash, verify_password
from app.models.user import User
from app.schemas.user import UserCreate

def get_user_by_email(db: Session, *, email: str) -> Optional[User]:
    """
    Retrieves a user from the database by their email.
    """
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, *, obj_in: UserCreate) -> User:
    """
    Creates a new user in the database.
    """
    # Create a dictionary from the input schema, excluding the plain password.
    db_obj_data = obj_in.dict(exclude={"password"})
    
    # Create the user model instance, adding the hashed password.
    db_obj = User(
        **db_obj_data,
        hashed_password=get_password_hash(obj_in.password)
    )
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def authenticate_user(db: Session, *, email: str, password: str) -> Optional[User]:
    """
    Authenticates a user.
    Returns the user object on success, None on failure.
    """
    user = get_user_by_email(db, email=email)
    if not user:
        return None
    # Cast to bool for static type checkers because model attributes are declared as Column[bool].
    user_is_active: bool = cast(bool, user.is_active)
    if not user_is_active:
        return None
    if not verify_password(password, cast(str, user.hashed_password)):
        return None
    return user