from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, List

from app.models.user import UserRole

# -- Base Schemas --
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    # --- CRUCIAL FIX 1: The type hint should be the FINAL type ---
    role: UserRole

# -- Schemas for API Input --
class UserCreate(UserBase):
    password: str

    # --- CRUCIAL FIX 2: Use a pre-validator ---
    # This validator runs BEFORE Pydantic's own validation.
    # It takes the raw string input and converts it to the Enum type the field expects.
    @field_validator("role", mode="before")
    @classmethod
    def role_to_enum(cls, v):
        if isinstance(v, str):
            try:
                return UserRole(v.lower())
            except ValueError:
                # This provides a clear error message if an invalid string is sent
                valid_roles = [e.value for e in UserRole]
                raise ValueError(f"'{v}' is not a valid role. Valid roles are: {valid_roles}")
        return v

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None

# -- Schemas for API Output --
class User(UserBase):
    id: int
    is_active: bool
    # 'role' is already the correct type from UserBase
    
    class Config:
        from_attributes = True
        
# -- Schema for Bulk Creation --
class UserBulkCreate(BaseModel):
    users: List[UserCreate]