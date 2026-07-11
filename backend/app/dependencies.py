from typing import Generator, List
from fastapi import Depends, HTTPException, status, Request
from jose import JWTError
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.config import settings
from app.utils.security import decode_token
from app.models.user import User

def get_db() -> Generator[Session, None, None]:
    """Dependency that yields a database session and closes it afterwards."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    """
    Dependency to retrieve the currently authenticated user from the database.
    Validates token presence, token structure, and expiration parameters.
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "success": False,
                "error": {
                    "code": "AUTH_REQUIRED",
                    "message": "Authentication required",
                    "details": None
                }
            }
        )

    parts = auth_header.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "success": False,
                "error": {
                    "code": "AUTH_INVALID_TOKEN",
                    "message": "Invalid or expired token",
                    "details": None
                }
            }
        )

    token = parts[1]
    try:
        payload = decode_token(token)
        
        # Verify token type is access
        if payload.get("type") != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "success": False,
                    "error": {
                        "code": "AUTH_INVALID_TOKEN",
                        "message": "Invalid or expired token",
                        "details": None
                    }
                }
            )

        user_id = payload.get("sub")
        if user_id is None:
            raise Exception()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "success": False,
                "error": {
                    "code": "AUTH_INVALID_TOKEN",
                    "message": "Invalid or expired token",
                    "details": None
                }
            }
        )

    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "success": False,
                "error": {
                    "code": "AUTH_INVALID_TOKEN",
                    "message": "Invalid or expired token",
                    "details": None
                }
            }
        )

    return user

def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Dependency that verifies that the currently logged-in user is active."""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "success": False,
                "error": {
                    "code": "AUTH_INACTIVE_USER",
                    "message": "User account is inactive",
                    "details": None
                }
            }
        )
    return current_user

class RoleRequired:
    """Role-based authorization dependency check."""
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_active_user)) -> User:
        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "success": False,
                    "error": {
                        "code": "AUTH_FORBIDDEN",
                        "message": f"Permission denied. Required role in {self.allowed_roles}",
                        "details": None
                    }
                }
            )
        return current_user
