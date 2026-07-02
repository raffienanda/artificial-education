from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional


# --- Auth ---
class UserResponse(BaseModel):
    id: int
    username: str
    display_name: Optional[str] = None
    role: str = "student"
    xp: int = 0
    combo: int = 0
    total_score: int = 0
    reward_points: int = 0
    current_streak: int = 0
    longest_streak: int = 0
    redeemed_rewards: List[str] = []
    level: int = 1
    xp_in_level: int = 0
    xp_to_next_level: int = 500

    class Config:
        from_attributes = True


class AuthRegister(BaseModel):
    username: str
    password: str
    display_name: Optional[str] = None


class AuthLogin(BaseModel):
    username: str
    password: str


class AuthToken(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

# --- Course, Module & Subtopic ---
class CourseResponse(BaseModel):
    id: str
    title: str
    description: str
    icon: str

    class Config:
        from_attributes = True


class SubtopicBase(BaseModel):
    id: str
    title: str
    content: Dict[str, Any]

class SubtopicResponse(SubtopicBase):
    class Config:
        from_attributes = True

class ModuleBase(BaseModel):
    id: str
    course_id: Optional[str] = None
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


class AdminQuestionCreate(BaseModel):
    subtopic_id: str
    question_text: str
    options: List[OptionSchema]
    correct_answer: str
    explanation: str
    difficulty: str = "mudah"


class AdminQuestionUpdate(BaseModel):
    subtopic_id: Optional[str] = None
    question_text: Optional[str] = None
    options: Optional[List[OptionSchema]] = None
    correct_answer: Optional[str] = None
    explanation: Optional[str] = None
    difficulty: Optional[str] = None


class AdminQuestionResponse(BaseModel):
    id: str
    subtopic_id: str
    question_text: str
    options: List[OptionSchema]
    correct_answer: str
    explanation: str
    difficulty: str

    class Config:
        from_attributes = True


class AdminSubtopicCreate(BaseModel):
    module_id: str
    title: str
    content: Dict[str, Any]


class AdminSubtopicUpdate(BaseModel):
    module_id: Optional[str] = None
    title: Optional[str] = None
    content: Optional[Dict[str, Any]] = None


class AdminSubtopicResponse(BaseModel):
    id: str
    module_id: str
    title: str
    content: Dict[str, Any]

    class Config:
        from_attributes = True


class AnswerSubmission(BaseModel):
    question_id: str
    selected_option_id: str
    user_id: int = 1 # hardcoded default for dummy user
    action: str = "easy_quiz"
    duration_seconds: int = 0

class AnswerFeedback(BaseModel):
    correct: bool
    correct_answer: str
    explanation: str
    reward_xp: int
    new_mastery: float
    q_value: float = 0.0
    learning_state: str = ""
    next_learning_state: str = ""
    user: UserResponse


# --- Gamification ---
class LeaderboardEntry(BaseModel):
    rank: int
    id: int
    username: str
    display_name: Optional[str] = None
    xp: int = 0
    level: int = 1
    total_score: int = 0
    reward_points: int = 0
    current_streak: int = 0


class RewardItem(BaseModel):
    id: str
    title: str
    description: str
    cost: int
    type: str


class RewardRedeemRequest(BaseModel):
    reward_id: str


class RewardRedeemResponse(BaseModel):
    success: bool
    message: str
    reward_points: int
    redeemed_rewards: List[str]
    user: UserResponse

# --- Progress ---
class ProgressResponse(BaseModel):
    topic_id: str
    mastery: float
    status: str

    class Config:
        from_attributes = True


# --- Learning Path Recommendation ---
class RecommendationRequest(BaseModel):
    user_id: int = 1
    current_module_id: str
    current_subtopic_id: str


class RecommendationResponse(BaseModel):
    macro_action: str
    recommended_module_id: str
    recommended_subtopic_id: str
    micro_action: str
    state: str
    q_values: Dict[str, float]
    reason: str


class InteractionLogResponse(BaseModel):
    subtopic_id: str
    state: str
    action: str
    reward: float
    score: float
    created_at: Any

    class Config:
        from_attributes = True


# --- Admin Prerequisites ---
class PrerequisiteCreate(BaseModel):
    topic_id: str
    prerequisite_id: str
    mastery_threshold: float = 60.0


class PrerequisiteUpdate(BaseModel):
    mastery_threshold: float


class PrerequisiteResponse(BaseModel):
    id: int
    topic_id: str
    prerequisite_id: str
    mastery_threshold: float

    class Config:
        from_attributes = True
