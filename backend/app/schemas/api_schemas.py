from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

# --- Module & Subtopic ---
class SubtopicBase(BaseModel):
    id: str
    title: str
    content: Dict[str, Any]

class SubtopicResponse(SubtopicBase):
    class Config:
        from_attributes = True

class ModuleBase(BaseModel):
    id: str
    title: str
    icon: str
    description: str
    difficulty: str
    estimated_time: str
    order: int
    status: str

class ModuleResponse(ModuleBase):
    subtopics: List[SubtopicResponse] = []
    
    class Config:
        from_attributes = True

# --- Question ---
class OptionSchema(BaseModel):
    id: str
    text: str
    label: str

class QuestionResponse(BaseModel):
    id: str
    subtopic_id: str
    question: str = Field(validation_alias='question_text')
    options: List[OptionSchema]
    # correct_answer and explanation are hidden from public fetch
    
    class Config:
        from_attributes = True
        populate_by_name = True

class AnswerSubmission(BaseModel):
    question_id: str
    selected_option_id: str
    user_id: int = 1 # hardcoded default for dummy user

class AnswerFeedback(BaseModel):
    correct: bool
    correct_answer: str
    explanation: str
    reward_xp: int
    new_mastery: float

# --- Progress ---
class ProgressResponse(BaseModel):
    topic_id: str
    mastery: float
    status: str

    class Config:
        from_attributes = True
