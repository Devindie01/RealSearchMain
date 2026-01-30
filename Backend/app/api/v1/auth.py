from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from fastapi.security import OAuth2PasswordRequestForm
from app.db.session import get_session
from app.models.user import User, UserCreate, UserPublic, Token
from app.core import security

router = APIRouter()


# signup route
@router.post("/signup", response_model=UserPublic)
def signup(user_in: UserCreate, db: Session = Depends(get_session)):
    # email already exists?
    statement = select(User).where(User.email == user_in.email.lower().strip())
    existing_user = db.exec(statement).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="User already registered")

    # user instance
    new_user = User(
        email=user_in.email.lower().strip(),
        full_name=user_in.full_name,
        hashed_password=security.hash_password(user_in.password),  # Scramble here!
        is_active=True,
    )

    # Save to the database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# Change response_model to dict or create a new LoginResponse schema
@router.post("/login")
async def login(
    db: Session = Depends(get_session), form_data: OAuth2PasswordRequestForm = Depends()
):
    # ... your existing logic to find the user ...
    statement = select(User).where(User.email == form_data.username.lower().strip())
    user = db.exec(statement).first()

    if not user or not security.verify_password(
        form_data.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    access_token = security.create_access_token(subject=user.email)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "email": user.email,
            "full_name": user.full_name,  # This provides the missing data
        },
    }
