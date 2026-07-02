from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base


class Course(Base):
    __tablename__ = "courses"

    id = Column(String, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    icon = Column(String)

    modules = relationship("Module", back_populates="course")


class Module(Base):
    __tablename__ = "modules"

    id = Column(String, primary_key=True, index=True) # e.g. mod-001
    course_id = Column(String, ForeignKey("courses.id"), nullable=True)
    title = Column(String)
    icon = Column(String)
    description = Column(String)
    difficulty = Column(String)
    estimated_time = Column(String)
    order = Column(Integer)
    status = Column(String, default="locked")

    course = relationship("Course", back_populates="modules")
    subtopics = relationship("Subtopic", back_populates="module")

class Subtopic(Base):
    __tablename__ = "subtopics"

    id = Column(String, primary_key=True, index=True) # e.g. sub-001-1
    module_id = Column(String, ForeignKey("modules.id"))
    title = Column(String)
    content = Column(JSON) # Store tabs and sections as JSON for flexibility
    
    module = relationship("Module", back_populates="subtopics")
    questions = relationship("Question", back_populates="subtopic")
