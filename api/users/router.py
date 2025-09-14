
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from core.security import create_access_token, verify_password
from . import schemas, services

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

@router.post("/register", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
async def register_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    """Endpoint to register a new user."""
    db_user = await services.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    return await services.create_user(db=db, user=user)


@router.post("/login", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    """Endpoint to login and get an access token."""
    user = await services.get_user_by_email(db, email=form_data.username) # OAuth2 form uses 'username' for email
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(
        data={"sub": user.email}
    )
    return {"access_token": access_token, "token_type": "bearer"}
