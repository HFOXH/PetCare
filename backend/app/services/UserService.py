import uuid
from datetime import datetime, timezone

from passlib.context import CryptContext
from sqlalchemy import select

from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse


# Password hashing context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a plain password using bcrypt."""
    return pwd_context.hash(password)


def register_user(db, email: str, full_name: str, password: str) -> User:
    """Register a new user with email, full_name, and hashed password."""
    # Check if user already exists
    stmt = select(User).where(User.email == email)
    existing = db.scalar(stmt)
    if existing:
        raise ValueError("Email already registered")
    hashed_pw = get_password_hash(password)
    user = User(
        email=email,
        full_name=full_name,
        password_hash=hashed_pw,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db, email: str, password: str) -> User | None:
    """Authenticate a user by email and password."""
    user = db.scalar(select(User).where(User.email == email))
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user


def fetch_users(db, skip: int = 0, limit: int = 100) -> list[User]:
    """Fetch a list of users with pagination."""
    stmt = select(User).offset(skip).limit(limit)
    return list(db.scalars(stmt).all())


def fetch_user(db, user_id: uuid.UUID) -> User | None:
    """Fetch a single user by ID."""
    return db.get(User, user_id)


def update_user(db, user: User, email: str | None = None, full_name: str | None = None) -> User:
    """Update user email and/or full_name."""
    if email is not None:
        user.email = email
    if full_name is not None:
        user.full_name = full_name
    db.commit()
    db.refresh(user)
    return user


def delete_user(db, user: User) -> None:
    """Delete a user."""
    db.delete(user)
    db.commit()