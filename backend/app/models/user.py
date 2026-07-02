from sqlalchemy import Column, Date, Integer, String, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    display_name = Column(String)
    password_hash = Column(String)
    role = Column(String, default="student")
    xp = Column(Integer, default=0)
    combo = Column(Integer, default=0)
    total_score = Column(Integer, default=0)
    reward_points = Column(Integer, default=0)
    current_streak = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    last_study_date = Column(Date, nullable=True)
    redeemed_rewards = Column(JSON, default=list)
    
    # Progress relationship
    progress = relationship("UserProgress", back_populates="user")

    @property
    def level(self):
        return (self.xp or 0) // 500 + 1

    @property
    def xp_in_level(self):
        return (self.xp or 0) % 500

    @property
    def xp_to_next_level(self):
        return 500
