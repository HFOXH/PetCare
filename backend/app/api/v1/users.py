import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.user import UserCreate, UserLogin, UserResponse, LoginResponse
from app.services.UserService import register_user, authenticate_user, fetch_users, fetch_user, update_user, delete_user
from app.security import create_access_token, get_current_user


router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    """Register a new user account."""
    try:
        user = register_user(db, email=user_data.email, full_name=user_data.full_name, password=user_data.password)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return user


@router.post(
    "/login",
    response_model=LoginResponse,
    summary="Login and receive JWT access token",
)
def login(
    login_data: UserLogin,
    db: Session = Depends(get_db),
):
    """Login with email and password to receive a JWT access token."""
    user = authenticate_user(db, email=login_data.email, password=login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    access_token = create_access_token(subject=user.id)
    return LoginResponse(access_token=access_token, user=user)


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user profile",
)
def get_current_user_profile(
    current_user=Depends(get_current_user),
):
    """Get the current authenticated user's profile."""
    return current_user


@router.get(
    "/",
    response_model=list[UserResponse],
    summary="List users",
)
def list_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """List all users."""
    users = fetch_users(db, skip=skip, limit=limit)
    return users


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Get user by ID",
)
def get_user(
    user_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    """Get a specific user by ID."""
    user = fetch_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    summary="Update user",
)
def update_user_endpoint(
    user_id: uuid.UUID,
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    """Update a user's email and full name."""
    user = fetch_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    updated = update_user(db, user, email=user_data.email, full_name=user_data.full_name)
    return user


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete user",
)
def delete_user_endpoint(
    user_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    """Delete a user."""
    user = fetch_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    delete_user(db, user)