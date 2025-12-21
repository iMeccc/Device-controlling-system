from datetime import datetime, timedelta
from typing import Any, Union, Optional
from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

# --- Password Hashing ---
# We use passlib to handle password hashing. 'bcrypt' is the chosen algorithm.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain password against its hashed version."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hashes a plain password."""
    return pwd_context.hash(password)


# --- JWT Token Handling ---
def create_access_token(
    subject: Union[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """
    Creates a JWT access token.
    :param subject: The subject of the token (e.g., user's email or id).
    :param expires_delta: Optional expiration delta. If not provided, uses the default from settings.
    :return: The encoded JWT token.
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

from jose import jwt, JWTError
from fastapi import HTTPException, status
from typing import Any

# --- JWT Token Decoding ---
def decode_access_token(token: str) -> str:
    """
    Decodes a JWT access token and returns its subject (user ID).
    Raises HTTPException if the token is invalid or expired.
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        
        # Get the subject from the payload. It can be of any type or None.
        sub: Any = payload.get("sub")
        
        # First, check if the subject exists at all.
        if sub is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials - token subject missing",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # If it exists, we can now safely return it as a string.
        # Pydantic and SQLAlchemy can handle the string representation of the user ID.
        return str(sub)

    except JWTError:
        # This catches errors like invalid signature, token has expired, etc.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials - invalid token or expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        # Catch any other unexpected errors during decoding
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials - token decoding failed: {e}",
            headers={"WWW-Authenticate": "Bearer"},
        )