from sqlalchemy.orm import Session
from typing import Optional, Dict, Any

from app.models.log import AccessLog

def create_log_entry(
    db: Session,
    *,
    user_id: Optional[int],
    action: str,
    details: Optional[Dict[str, Any]] = None,
) -> AccessLog:
    """
    Create a new entry in the access log.
    """
    log_entry = AccessLog(
        user_id=user_id,
        action=action,
        details=details,
    )
    db.add(log_entry)
    db.commit()
    db.refresh(log_entry)
    return log_entry