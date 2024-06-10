from models import post as post_model
from schemas import post as post_schema
from sqlalchemy.orm import Session

def create_post(db: Session, post: post_schema.PostCreate, user_id: int):
    """
    Create a new post.

    - **db**: The database session.
    - **post**: The post data.
    - **user_id**: The ID of the user creating the post.

    Returns the created post.
    """
    db_post = post_model.Post(**post.dict(), user_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def get_user_posts(db: Session, user_id: int):
    """
    Retrieve all posts of a user.

    - **db**: The database session.
    - **user_id**: The ID of the user.

    Returns a list of posts.
    """
    return db.query(post_model.Post).filter(post_model.Post.user_id == user_id).all()

def delete_post(db: Session, post_id: int):
    """
    Delete a post by ID.

    - **db**: The database session.
    - **post_id**: The ID of the post to delete.

    Returns True if the post was deleted, otherwise False.
    """
    db_post = db.query(post_model.Post).filter(post_model.Post.id == post_id).first()
    if db_post:
        db.delete(db_post)
        db.commit()
        return True
    return False
