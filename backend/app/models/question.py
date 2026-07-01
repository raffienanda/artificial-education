from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base

class Question(Base):
    __tablename__ = "questions"

    id = Column(String, primary_key=True, index=True) # e.g. q-001
    subtopic_id = Column(String, ForeignKey("subtopics.id"))
    question_text = Column(String)
    options = Column(JSON) # Array of {id: 'a', text: '...', label: 'A'}
    correct_answer = Column(String)
    explanation = Column(String)
    difficulty = Column(String)
    
    subtopic = relationship("Subtopic", back_populates="questions")
