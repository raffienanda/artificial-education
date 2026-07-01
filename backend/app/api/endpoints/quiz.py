from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.question import Question
from app.models.progress import UserProgress
from app.models.user import User
from app.schemas.api_schemas import QuestionResponse, AnswerSubmission, AnswerFeedback
from app.ml.q_learning import q_agent
from typing import List

router = APIRouter()

@router.get("/{module_id}", response_model=List[QuestionResponse])
def get_questions(module_id: str, db: Session = Depends(get_db)):
    # We fetch questions related to subtopics inside this module
    from app.models.module import Subtopic
    subtopics = db.query(Subtopic).filter(Subtopic.module_id == module_id).all()
    subtopic_ids = [s.id for s in subtopics]
    
    questions = db.query(Question).filter(Question.subtopic_id.in_(subtopic_ids)).all()
    return questions

@router.post("/submit", response_model=AnswerFeedback)
def submit_answer(submission: AnswerSubmission, db: Session = Depends(get_db)):
    question = db.query(Question).filter(Question.id == submission.question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
        
    user = db.query(User).filter(User.id == submission.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    is_correct = (question.correct_answer == submission.selected_option_id)
    
    # Track combo and score
    if is_correct:
        user.combo += 1
        user.total_score += 1
    else:
        user.combo = 0
        
    # Q-Learning: Calculate reward
    reward = q_agent.calculate_reward(is_correct, user.combo)
    user.xp += int(reward)
    if user.xp < 0: user.xp = 0
    
    # Progress & BKT Update
    progress = db.query(UserProgress).filter(
        UserProgress.user_id == user.id, 
        UserProgress.topic_id == question.subtopic_id
    ).first()
    
    new_mastery = 0.0
    if progress:
        # Update BKT
        progress.p_known = q_agent.update_bkt(
            is_correct, progress.p_known, progress.p_learn, progress.p_guess, progress.p_slip
        )
        # Update Mastery (Simplified)
        if is_correct:
            progress.mastery = min(100.0, progress.mastery + 5.0)
        new_mastery = progress.mastery
        
    db.commit()
    
    return AnswerFeedback(
        correct=is_correct,
        correct_answer=question.correct_answer,
        explanation=question.explanation,
        reward_xp=int(reward),
        new_mastery=new_mastery
    )
