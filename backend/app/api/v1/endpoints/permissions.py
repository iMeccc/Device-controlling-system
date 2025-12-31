from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Any

from app.crud import crud_permission
from app.schemas.permission import PermissionGrant
from app.schemas.user import User
from app.api import deps

router = APIRouter()

@router.post("/grant", response_model=User)
def grant_permission_to_user(
    permission_in: PermissionGrant,
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_active_admin),
) -> Any:
    """
    Grant a user permission for an instrument using their ID (Admins only).
    """
    # --- CRUCIAL FIX: Call the correct function name ---
    updated_user = crud_permission.grant_permission(db=db, permission_in=permission_in)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User or Instrument not found")
    return updated_user

@router.post("/revoke", response_model=User)
def revoke_permission_from_user(
    permission_in: PermissionGrant,
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_active_admin),
) -> Any:
    """
    Revoke a user's permission for an instrument using their ID (Admins only).
    """
    # --- CRUCIAL FIX: Call the correct function name ---
    updated_user = crud_permission.revoke_permission(db=db, permission_in=permission_in)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User or Instrument not found")
    return updated_user