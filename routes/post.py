from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from services import post as post_service
from schemas import post as post_schema
from jose import JWTError, jwt
from app.config import SessionLocal, SECRET_KEY, ALGORITHM
from models.user import User  # Ensure User is imported
import cachetools
from typing import List

from fastapi.security import OAuth2PasswordBearer

router = APIRouter()
cache = cachetools.TTLCache(maxsize=100, ttl=300)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Validate JWT token and return the current user.

    - **token**: The JWT token of the user.

    Returns the user details.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.email == token_data.email).first()
    if user is None:
        raise credentials_exception
    return user

@router.post("/addpost", response_model=post_schema.PostOut, summary="Add a Post", description="Add a new post. Validates payload size and requires authentication.")
def add_post(post: post_schema.PostCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Add a new post.

    - **text**: The content of the post.
    - **token**: The JWT token of the user.

    Validates the payload size (limit to 1 MB) and saves the post in memory. Returns the created post details.
    """
    if len(post.text.encode('utf-8')) > 1_000_000:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Payload too large")
    db_post = post_service.create_post(db, post, current_user.id)
    return db_post

@router.get("/posts", response_model=List[post_schema.PostOut], summary="Get Posts", description="Retrieve all posts of the authenticated user with caching for 5 minutes.")
def get_posts(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Retrieve all posts of the authenticated user.

    - **token**: The JWT token of the user.

    Returns all posts of the user. Implements response caching for up to 5 minutes.
    """
    if current_user.id in cache:
        return cache[current_user.id]
    posts = post_service.get_user_posts(db, current_user.id)
    cache[current_user.id] = posts
    return posts

@router.delete("/deletepost/{post_id}", summary="Delete a Post", description="Delete a specific post by post ID. Requires authentication.")
def delete_post(post_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Delete a specific post.

    - **post_id**: The ID of the post to delete.
    - **token**: The JWT token of the user.

    Deletes the corresponding post from memory.
    """
    post = db.query(post_model.Post).filter(post_model.Post.id == post_id, post_model.Post.user_id == current_user.id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    post_service.delete_post(db, post_id)
    return {"detail": "Post deleted"}
