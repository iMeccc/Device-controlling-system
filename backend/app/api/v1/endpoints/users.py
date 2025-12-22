from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Any, List
from pydantic import EmailStr # <-- Added import

from app.crud import crud_user
from app.schemas.user import User, UserCreate, UserBulkCreate
from app.schemas.token import Token
from app.api import deps
from app.core.security import create_access_token

router = APIRouter()

@router.post(
    "/",
    response_model=User, 
    tags=["Users"],
    dependencies=[Depends(deps.get_current_active_admin)]
)
def create_user(
    user_in: UserCreate,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Create new user (Admins only).
    """
    user = crud_user.get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    user = crud_user.create_user(db=db, obj_in=user_in)
    return user

@router.post(
    "/login/access-token", 
    response_model=Token, 
    tags=["Users"],
    description="获取访问令牌以进行后续请求。**注意**: 'username' 字段需要填写您注册时使用的 **电子邮件地址**。"
)
def login_for_access_token(
    db: Session = Depends(deps.get_db), 
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    user = crud_user.authenticate_user(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(subject=user.id)
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }

@router.post(
    "/bulk-create",
    response_model=List[User],
    tags=["Users"],
    dependencies=[Depends(deps.get_current_active_admin)],
)
def create_users_bulk(
    users_in: UserBulkCreate,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Create multiple new users in the system (Admins only).
    """
    created_users = crud_user.create_multi(db=db, users_in=users_in.users)
    return created_users

# --- NEW FUNCTION ADDED HERE ---
@router.delete(
    "/{user_email}",
    response_model=User,
    tags=["Users"],
    dependencies=[Depends(deps.get_current_active_admin)],
)
def delete_user(
    user_email: EmailStr,
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_active_admin),
) -> Any:
    """
    Delete a user by their email (Admins only).
    """
    user_to_delete = crud_user.get_user_by_email(db, email=user_email)
    if not user_to_delete:
        raise HTTPException(status_code=404, detail="User with this email not found")
    
    if user_to_delete.id == current_admin.id:
        raise HTTPException(status_code=400, detail="Admins cannot delete their own account")
        
    deleted_user = crud_user.remove(db=db, id=user_to_delete.id)
    return deleted_user