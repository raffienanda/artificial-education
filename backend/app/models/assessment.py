from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, UniqueConstraint, func
from sqlalchemy.orm import relationship

from app.core.database import Base


class AssessmentAttempt(Base):
    __tablename__ = "assessment_attempts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    module_id = Column(String, ForeignKey("modules.id"), nullable=False, index=True)
    subtopic_id = Column(String, ForeignKey("subtopics.id"), nullable=True, index=True)
    assessment_type = Column(String, nullable=False, index=True)
    score = Column(Integer, default=0)
    total_questions = Column(Integer, default=0)
    percentage = Column(Float, default=0.0)
    passed = Column(Boolean, default=False)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    finished_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship("User")
    module = relationship("Module")
    subtopic = relationship("Subtopic")
    answers = relationship("AssessmentAnswer", back_populates="attempt", cascade="all, delete-orphan")


class AssessmentAnswer(Base):
    __tablename__ = "assessment_answers"

    id = Column(Integer, primary_key=True, index=True)
    attempt_id = Column(Integer, ForeignKey("assessment_attempts.id"), nullable=False, index=True)
    question_id = Column(String, ForeignKey("questions.id"), nullable=False, index=True)
    selected_option_id = Column(String, nullable=False)
    is_correct = Column(Boolean, default=False)
    duration_seconds = Column(Integer, default=0)
    answered_at = Column(DateTime(timezone=True), server_default=func.now())

    attempt = relationship("AssessmentAttempt", back_populates="answers")
    question = relationship("Question")

    __table_args__ = (
        UniqueConstraint("attempt_id", "question_id", name="uq_attempt_question_answer"),
    )
