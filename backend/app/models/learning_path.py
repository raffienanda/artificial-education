from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, UniqueConstraint, func
from sqlalchemy.orm import relationship
from app.core.database import Base


class TopicPrerequisite(Base):
    __tablename__ = "topic_prerequisites"

    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(String, ForeignKey("modules.id"), nullable=False)
    prerequisite_id = Column(String, ForeignKey("modules.id"), nullable=False)
    mastery_threshold = Column(Float, default=60.0)

    topic = relationship("Module", foreign_keys=[topic_id])
    prerequisite = relationship("Module", foreign_keys=[prerequisite_id])

    __table_args__ = (
        UniqueConstraint("topic_id", "prerequisite_id", name="uq_topic_prerequisite"),
    )


class QValue(Base):
    __tablename__ = "q_values"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    subtopic_id = Column(String, ForeignKey("subtopics.id"), nullable=False)
    state = Column(String, nullable=False)
    action = Column(String, nullable=False)
    value = Column(Float, default=0.0)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User")
    subtopic = relationship("Subtopic")

    __table_args__ = (
        UniqueConstraint("user_id", "subtopic_id", "state", "action", name="uq_q_value_state_action"),
    )


class InteractionLog(Base):
    __tablename__ = "interaction_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    subtopic_id = Column(String, ForeignKey("subtopics.id"), nullable=False)
    state = Column(String, nullable=False)
    action = Column(String, nullable=False)
    reward = Column(Float, default=0.0)
    score = Column(Float, default=0.0)
    duration_seconds = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User")
    subtopic = relationship("Subtopic")
