from pydantic import BaseModel, EmailStr

class PermissionBase(BaseModel):
    instrument_id: int

class PermissionGrant(PermissionBase):
    user_id: int

# We keep the original for internal use if needed, though not required by the API now
class PermissionCreate(PermissionBase):
    user_id: int