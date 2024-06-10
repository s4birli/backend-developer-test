from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.config import Base

class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(1000))
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User")
