from sqlalchemy.orm import Session
from typing import Optional, List, cast

from app.core.security import get_password_hash, verify_password
from app.models.user import User, UserRole
from app.schemas.user import UserCreate

def get(db: Session, id: int) -> Optional[User]:
    return db.query(User).filter(User.id == id).first()

def get_user_by_email(db: Session, *, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, *, obj_in: UserCreate) -> User:
    db_obj_data = obj_in.dict(exclude={"password"})
    db_obj = User(
        **db_obj_data,
        hashed_password=get_password_hash(obj_in.password)
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def authenticate_user(db: Session, *, email: str, password: str) -> Optional[User]:
    user = get_user_by_email(db, email=email)
    if not user: return None
    if user.is_active is False: return None
    if not verify_password(password, user.hashed_password): return None
    return user

def create_multi(db: Session, *, users_in: List[UserCreate]) -> List[User]:
    created_users: List[User] = []
    for user_in in users_in:
        existing_user = get_user_by_email(db, email=user_in.email)
        if existing_user:
            continue
        user = create_user(db=db, obj_in=user_in)
        created_users.append(user)
    return created_users

def remove(db: Session, *, id: int) -> User | None:
    user_to_delete = db.query(User).get(id)
    if user_to_delete:
        db.delete(user_to_delete)
        db.commit()
    return user_to_delete

def get_multi(db: Session, *, skip: int = 0, limit: int = 100) -> List[User]:
    return db.query(User).offset(skip).limit(limit).all()

from app.schemas.user import UserUpdate # Add this to your imports

def update(db: Session, *, db_obj: User, obj_in: UserUpdate) -> User:
    """
    Update a user's data.
    """
    update_data = obj_in.dict(exclude_unset=True)

    if "password" in update_data and update_data["password"]:
        hashed_password = get_password_hash(update_data["password"])
        db_obj.hashed_password = hashed_password
    
    if "full_name" in update_data:
        db_obj.full_name = update_data["full_name"]
        
    if "role" in update_data:
        db_obj.role = UserRole(update_data["role"])

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj