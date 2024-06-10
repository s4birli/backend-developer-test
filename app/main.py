from fastapi import FastAPI
from routes import auth as auth_routes
from routes import post as post_routes
from app.config import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI Application",
    description="This is a FastAPI application following the MVC pattern.",
    version="1.0.0",
    contact={
        "name": "Developer",
        "email": "developer@example.com",
    },
)

app.include_router(auth_routes.router, prefix="/auth", tags=["auth"])
app.include_router(post_routes.router, prefix="/posts", tags=["posts"])
