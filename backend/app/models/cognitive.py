from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import relationship

from app.core.database import Base


class CognitiveItem(Base):
    __tablename__ = "cognitive_items"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, nullable=False, index=True)
    stage = Column(String, nullable=False, index=True)
    statement = Column(Text, nullable=False)


class CognitiveResponse(Base):
    __tablename__ = "cognitive_responses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    item_id = Column(Integer, ForeignKey("cognitive_items.id"), nullable=False, index=True)
    score = Column(Integer, nullable=False)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User")
    item = relationship("CognitiveItem")

    __table_args__ = (
        UniqueConstraint("user_id", "item_id", name="uq_user_cognitive_item"),
    )


class CognitiveProfile(Base):
    __tablename__ = "cognitive_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True, index=True)
    dualism_score = Column(Float, default=0.0)
    multiplicity_score = Column(Float, default=0.0)
    relativism_score = Column(Float, default=0.0)
    commitment_score = Column(Float, default=0.0)
    dominant_stage = Column(String, default="dualism")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User")
