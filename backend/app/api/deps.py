from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import decode_access_token
from app.crud import crud_user
from app.db.session import get_db
from app.models.user import User

# This is a "dependency" that can be injected into our path operations.
# It tells FastAPI two things:
# 1. Look for an "Authorization" header in the request.
# 2. Check if the value is "Bearer <some_token>".
# The 'tokenUrl' points to our login endpoint, which is used by the interactive docs.
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/users/login/access-token"
)

def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> User:
    """
    Dependency to get the current user from a token.
    1. Decodes the token to get the user ID.
    2. Fetches the user from the database.
    3. Checks if the user exists and is active.
    4. Returns the user object.
    Raises HTTPException if any step fails.
    """
    try:
        user_id_str = decode_access_token(token)
        # It's possible the user_id is not a valid integer
        user_id = int(user_id_str)
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user ID in token",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    user = crud_user.get(db, id=user_id)
    
    # First, check if the user exists at all.
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Then, perform the explicit check on the is_active attribute.
    if user.is_active is False:
        raise HTTPException(status_code=400, detail="Inactive user")
        
    return user

def get_current_active_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Dependency to get the current user and check if they are an admin.
    - Reuses the 'get_current_user' dependency.
    - Checks the 'role' attribute of the user.
    - Raises HTTPException 403 if the user is not an admin.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user
