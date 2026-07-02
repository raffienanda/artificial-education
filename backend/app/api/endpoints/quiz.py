from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date, timedelta
from app.core.database import get_db
from app.models.question import Question
from app.models.user import User
from app.core.security import get_optional_current_user
from app.schemas.api_schemas import QuestionResponse, AnswerSubmission, AnswerFeedback
from app.services.learning_path import record_q_learning_update
from typing import List

router = APIRouter()

@router.get("/{module_id}", response_model=List[QuestionResponse])
def get_questions(module_id: str, difficulty: str | None = None, db: Session = Depends(get_db)):
    # We fetch questions related to subtopics inside this module
    from app.models.module import Subtopic
    subtopics = db.query(Subtopic).filter(Subtopic.module_id == module_id).all()
    subtopic_ids = [s.id for s in subtopics]
    
    query = db.query(Question).filter(Question.subtopic_id.in_(subtopic_ids))
    if difficulty:
        filtered_query = query.filter(Question.difficulty == difficulty)
        questions = filtered_query.all()
        if questions:
            return questions

    questions = query.all()
    return questions

@router.post("/submit", response_model=AnswerFeedback)
def submit_answer(
    submission: AnswerSubmission,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_optional_current_user),
):
    question = db.query(Question).filter(Question.id == submission.question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
        
    user_id = current_user.id if current_user else submission.user_id
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    is_correct = (question.correct_answer == submission.selected_option_id)
    today = date.today()
    if user.last_study_date != today:
        if user.last_study_date == today - timedelta(days=1):
            user.current_streak += 1
        else:
            user.current_streak = 1
        user.longest_streak = max(user.longest_streak or 0, user.current_streak)
        user.last_study_date = today
    
    # Track combo and score
    if is_correct:
        user.combo = (user.combo or 0) + 1
        user.total_score = (user.total_score or 0) + 1
        user.reward_points = (user.reward_points or 0) + 10 + min(user.combo, 5)
    else:
        user.combo = 0
        
    learning_update = record_q_learning_update(
        db=db,
        user_id=user.id,
        subtopic_id=question.subtopic_id,
        is_correct=is_correct,
        selected_action=submission.action,
        duration_seconds=submission.duration_seconds,
    )

    xp_delta = max(0, int(learning_update["reward"]))
    user.xp = (user.xp or 0) + xp_delta

    db.commit()
    db.refresh(user)
    
    return AnswerFeedback(
        correct=is_correct,
        correct_answer=question.correct_answer,
        explanation=question.explanation,
        reward_xp=xp_delta,
        new_mastery=learning_update["new_mastery"],
        q_value=learning_update["q_value"],
        learning_state=learning_update["state"],
        next_learning_state=learning_update["next_state"],
        user=user,
    )
