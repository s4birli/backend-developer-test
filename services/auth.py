from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from models import user as user_model
from schemas import user as user_schema
from sqlalchemy.orm import Session

SECRET_KEY = "SECRET_KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    """
    Hash a plaintext password.

    - **password**: The plaintext password.

    Returns the hashed password.
    """
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    """
    Verify a plaintext password against a hashed password.

    - **plain_password**: The plaintext password.
    - **hashed_password**: The hashed password.

    Returns True if the password matches, otherwise False.
    """
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Create a JWT token.

    - **data**: The data to include in the token.
    - **expires_delta**: The expiration time of the token.

    Returns the encoded JWT token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def authenticate_user(db: Session, email: str, password: str):
    """
    Authenticate a user by email and password.

    - **db**: The database session.
    - **email**: The email of the user.
    - **password**: The password of the user.

    Returns the authenticated user if successful, otherwise False.
    """
    user = db.query(user_model.User).filter(user_model.User.email == email).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_user(db: Session, user: user_schema.UserCreate):
    """
    Create a new user.

    - **db**: The database session.
    - **user**: The user data.

    Returns the created user.
    """
    hashed_password = get_password_hash(user.password)
    db_user = user_model.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
