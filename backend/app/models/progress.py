from sqlalchemy import Column, Integer, String, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base

class UserProgress(Base):
    __tablename__ = "user_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    topic_id = Column(String) # Maps to subtopic_id or module_id conceptually
    mastery = Column(Float, default=0.0) # 0 to 100
    status = Column(String, default="learning")
    
    # BKT Parameters
    p_known = Column(Float, default=0.1)
    p_learn = Column(Float, default=0.2)
    p_guess = Column(Float, default=0.25)
    p_slip = Column(Float, default=0.1)
    
    user = relationship("User", back_populates="progress")
