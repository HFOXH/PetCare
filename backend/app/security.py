import uuid
from datetime import datetime, timedelta, timezone

from jwt import PyJWTError
import bcrypt
from fastapi.security import OAuth2PasswordBearer

from app.core.config import settings
from app.models.user import User
from app.schemas.user import UserResponse
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db

# JWT settings from environment or defaults
SECRET_KEY = settings.secret_key if hasattr(settings, "secret_key") else "super-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login")


def create_access_token(subject: uuid.UUID | str, expires_delta: timedelta | None = None) -> str:
    """Create a JWT access token for a subject (user ID)."""
    if isinstance(subject, uuid.UUID):
        subject_str = str(subject)
    else:
        subject_str = str(subject)

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expire, "sub": subject_str, "iat": datetime.now(timezone.utc)}
    encoded_jwt = jwt_encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def jwt_encode(data: dict, key: str, algorithm: str = "HS256") -> str:
    """Encode a JWT token."""
    import jwt as pyjwt
    return pyjwt.encode(data, key, algorithm=algorithm)


def decode_access_token(token: str) -> dict:
    """Decode and validate a JWT token, returning the payload."""
    try:
        payload = jwt_decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except PyJWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def jwt_decode(token: str, key: str, algorithms: list = ["HS256"]) -> dict:
    """Decode a JWT token."""
    import jwt as pyjwt
    return pyjwt.decode(token, key, algorithms=algorithms)


def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
) -> User:
    """Dependency: get the current authenticated user from a JWT token."""
    payload = decode_access_token(token)
    user_id: str = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        user_uuid = uuid.UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user ID in token",
        )
    user = db.get(User, user_uuid)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    return user