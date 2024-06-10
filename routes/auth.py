from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from services import auth as auth_service
from schemas import user as user_schema
from app.config import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/signup", response_model=user_schema.UserOut, summary="User Signup", description="Create a new user account and return the user details.")
def signup(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user account.

    - **email**: The email of the user.
    - **password**: The password of the user.

    Returns the created user details.
    """
    db_user = auth_service.create_user(db, user)
    return db_user

@router.post("/login", summary="User Login", description="Authenticate a user and return a JWT token.")
def login(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    """
    Authenticate a user.

    - **email**: The email of the user.
    - **password**: The password of the user.

    Returns a JWT token upon successful authentication.
    """
    db_user = auth_service.authenticate_user(db, user.email, user.password)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = auth_service.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
