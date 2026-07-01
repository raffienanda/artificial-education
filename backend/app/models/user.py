from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    xp = Column(Integer, default=0)
    combo = Column(Integer, default=0)
    total_score = Column(Integer, default=0)
    
    # Progress relationship
    progress = relationship("UserProgress", back_populates="user")
