from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date, datetime, timedelta, timezone
from app.core.database import get_db
from app.models.assessment import AssessmentAnswer, AssessmentAttempt
from app.models.knowledge import KnowledgeState
from app.models.learning_path import TopicPrerequisite
from app.models.module import Module, Subtopic
from app.models.progress import UserProgress
from app.models.question import Question
from app.models.user import User
from app.core.security import get_optional_current_user
from app.schemas.api_schemas import QuestionResponse, AnswerSubmission, AnswerFeedback
from app.services.learning_path import record_q_learning_update
from typing import List

router = APIRouter()


def _get_question_module(db: Session, question: Question) -> Subtopic:
    subtopic = db.query(Subtopic).filter(Subtopic.id == question.subtopic_id).first()
    if not subtopic:
        raise HTTPException(status_code=404, detail="Subtopic not found")
    return subtopic


def _total_questions_for_assessment(db: Session, module_id: str, subtopic_id: str | None, assessment_type: str) -> int:
    subtopic_ids_query = db.query(Subtopic.id).filter(Subtopic.module_id == module_id)
    if assessment_type in ("drill", "quiz") and subtopic_id:
        subtopic_ids_query = subtopic_ids_query.filter(Subtopic.id == subtopic_id)

    subtopic_ids = [row.id for row in subtopic_ids_query.all()]
    return db.query(Question).filter(
        Question.subtopic_id.in_(subtopic_ids),
        Question.assessment_type == assessment_type,
    ).count()


def _record_assessment_answer(
    db: Session,
    user_id: int,
    question: Question,
    selected_option_id: str,
    is_correct: bool,
    duration_seconds: int,
) -> AssessmentAttempt:
    subtopic = _get_question_module(db, question)
    assessment_type = question.assessment_type or "quiz"
    attempt_subtopic_id = question.subtopic_id if assessment_type in ("drill", "quiz") else None
    total_questions = _total_questions_for_assessment(
        db=db,
        module_id=subtopic.module_id,
        subtopic_id=attempt_subtopic_id,
        assessment_type=assessment_type,
    )

    attempt = db.query(AssessmentAttempt).filter(
        AssessmentAttempt.user_id == user_id,
        AssessmentAttempt.module_id == subtopic.module_id,
        AssessmentAttempt.assessment_type == assessment_type,
        AssessmentAttempt.subtopic_id == attempt_subtopic_id,
        AssessmentAttempt.finished_at.is_(None),
    ).order_by(AssessmentAttempt.started_at.desc()).first()

    if not attempt:
        attempt = AssessmentAttempt(
            user_id=user_id,
            module_id=subtopic.module_id,
            subtopic_id=attempt_subtopic_id,
            assessment_type=assessment_type,
            total_questions=total_questions,
        )
        db.add(attempt)
        db.flush()

    answer = db.query(AssessmentAnswer).filter(
        AssessmentAnswer.attempt_id == attempt.id,
        AssessmentAnswer.question_id == question.id,
    ).first()

    if not answer:
        answer = AssessmentAnswer(
            attempt_id=attempt.id,
            question_id=question.id,
            selected_option_id=selected_option_id,
            is_correct=is_correct,
            duration_seconds=duration_seconds,
        )
        db.add(answer)
    else:
        answer.selected_option_id = selected_option_id
        answer.is_correct = is_correct
        answer.duration_seconds = duration_seconds
        answer.answered_at = datetime.now(timezone.utc)

    db.flush()
    answers = db.query(AssessmentAnswer).filter(AssessmentAnswer.attempt_id == attempt.id).all()
    attempt.score = sum(1 for item in answers if item.is_correct)
    attempt.total_questions = total_questions
    attempt.percentage = round((attempt.score / total_questions) * 100, 2) if total_questions else 0.0
    attempt.passed = attempt.percentage >= 60.0 if assessment_type in ("quiz", "post_test") else False
    if total_questions and len(answers) >= total_questions:
        attempt.finished_at = datetime.now(timezone.utc)

    return attempt


def _upsert_knowledge_state(db: Session, user_id: int, node_id: str, node_type: str, value: float, source: str) -> None:
    state = db.query(KnowledgeState).filter(
        KnowledgeState.user_id == user_id,
        KnowledgeState.node_id == node_id,
        KnowledgeState.node_type == node_type,
    ).first()

    if not state:
        state = KnowledgeState(
            user_id=user_id,
            node_id=node_id,
            node_type=node_type,
            state_value=value,
            source=source,
        )
        db.add(state)
        return

    state.state_value = value
    state.source = source


def _module_passed(db: Session, user_id: int, module_id: str) -> bool:
    module = db.query(Module).filter(Module.id == module_id).first()
    if not module:
        return False

    subtopic_ids = [subtopic.id for subtopic in module.subtopics]
    if not subtopic_ids:
        return False

    post_test_done = db.query(AssessmentAttempt).filter(
        AssessmentAttempt.user_id == user_id,
        AssessmentAttempt.module_id == module_id,
        AssessmentAttempt.assessment_type == "post_test",
        AssessmentAttempt.finished_at.isnot(None),
        AssessmentAttempt.passed.is_(True),
    ).first() is not None
    if not post_test_done:
        return False

    progress_rows = db.query(UserProgress).filter(
        UserProgress.user_id == user_id,
        UserProgress.topic_id.in_(subtopic_ids),
    ).all()
    progress_by_subtopic = {row.topic_id: row.mastery for row in progress_rows}
    average_mastery = sum(progress_by_subtopic.get(subtopic_id, 0.0) for subtopic_id in subtopic_ids) / len(subtopic_ids)
    return average_mastery >= 60.0


def _module_unlocked(db: Session, user_id: int, module_id: str) -> bool:
    module = db.query(Module).filter(Module.id == module_id).first()
    if not module:
        return False
    if (module.order or 1) <= 1:
        return True

    prerequisites = db.query(TopicPrerequisite).filter(TopicPrerequisite.topic_id == module_id).all()
    if prerequisites:
        return all(_module_passed(db=db, user_id=user_id, module_id=item.prerequisite_id) for item in prerequisites)

    previous_module = db.query(Module).filter(Module.order == (module.order or 1) - 1).first()
    return bool(previous_module and _module_passed(db=db, user_id=user_id, module_id=previous_module.id))


def _completed_pretest(db: Session, user_id: int, module_id: str) -> bool:
    return db.query(AssessmentAttempt).filter(
        AssessmentAttempt.user_id == user_id,
        AssessmentAttempt.module_id == module_id,
        AssessmentAttempt.assessment_type == "pre_test",
        AssessmentAttempt.finished_at.isnot(None),
    ).first() is not None


def _passed_assessment(
    db: Session,
    user_id: int,
    module_id: str,
    assessment_type: str,
    subtopic_id: str | None = None,
) -> bool:
    query = db.query(AssessmentAttempt).filter(
        AssessmentAttempt.user_id == user_id,
        AssessmentAttempt.module_id == module_id,
        AssessmentAttempt.assessment_type == assessment_type,
        AssessmentAttempt.finished_at.isnot(None),
        AssessmentAttempt.passed.is_(True),
    )
    if assessment_type in ("quiz", "drill"):
        query = query.filter(AssessmentAttempt.subtopic_id == subtopic_id)
    return query.first() is not None


def _completed_previous_quizzes(db: Session, user_id: int, module_id: str, subtopic_id: str | None) -> bool:
    if not subtopic_id:
        return True

    subtopics = db.query(Subtopic).filter(Subtopic.module_id == module_id).order_by(Subtopic.id).all()
    target_index = next((index for index, item in enumerate(subtopics) if item.id == subtopic_id), -1)
    if target_index <= 0:
        return True

    previous_ids = [item.id for item in subtopics[:target_index]]
    finished_count = db.query(AssessmentAttempt).filter(
        AssessmentAttempt.user_id == user_id,
        AssessmentAttempt.module_id == module_id,
        AssessmentAttempt.subtopic_id.in_(previous_ids),
        AssessmentAttempt.assessment_type == "quiz",
        AssessmentAttempt.finished_at.isnot(None),
        AssessmentAttempt.passed.is_(True),
    ).count()
    return finished_count >= len(previous_ids)


def _ensure_assessment_unlocked(
    db: Session,
    user_id: int,
    module_id: str,
    assessment_type: str,
    subtopic_id: str | None,
) -> None:
    if not _module_unlocked(db=db, user_id=user_id, module_id=module_id):
        raise HTTPException(status_code=403, detail="Modul masih terkunci")

    if assessment_type == "pre_test":
        return

    if not _completed_pretest(db=db, user_id=user_id, module_id=module_id):
        raise HTTPException(status_code=403, detail="Pre test modul harus diselesaikan terlebih dahulu")

    if assessment_type == "quiz" and _passed_assessment(
        db=db,
        user_id=user_id,
        module_id=module_id,
        assessment_type="quiz",
        subtopic_id=subtopic_id,
    ):
        raise HTTPException(status_code=403, detail="Quiz subtopik ini sudah lulus dan tidak bisa diulang")

    if assessment_type == "post_test" and _passed_assessment(
        db=db,
        user_id=user_id,
        module_id=module_id,
        assessment_type="post_test",
    ):
        raise HTTPException(status_code=403, detail="Post test modul ini sudah lulus dan tidak bisa diulang")

    if assessment_type == "quiz" and not _completed_previous_quizzes(
        db=db,
        user_id=user_id,
        module_id=module_id,
        subtopic_id=subtopic_id,
    ):
        raise HTTPException(status_code=403, detail="Selesaikan quiz subtopik sebelumnya terlebih dahulu")

    if assessment_type == "post_test":
        subtopic_ids = [row.id for row in db.query(Subtopic.id).filter(Subtopic.module_id == module_id).all()]
        finished_count = db.query(AssessmentAttempt).filter(
            AssessmentAttempt.user_id == user_id,
            AssessmentAttempt.module_id == module_id,
            AssessmentAttempt.subtopic_id.in_(subtopic_ids),
            AssessmentAttempt.assessment_type == "quiz",
            AssessmentAttempt.finished_at.isnot(None),
            AssessmentAttempt.passed.is_(True),
        ).count()
        if finished_count < len(subtopic_ids):
            raise HTTPException(status_code=403, detail="Selesaikan semua quiz subtopik sebelum post test")

@router.get("/{module_id}", response_model=List[QuestionResponse])
def get_questions(
    module_id: str,
    difficulty: str | None = None,
    assessment_type: str = "quiz",
    subtopic_id: str | None = None,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_optional_current_user),
):
    if current_user:
        _ensure_assessment_unlocked(
            db=db,
            user_id=current_user.id,
            module_id=module_id,
            assessment_type=assessment_type,
            subtopic_id=subtopic_id,
        )

    # We fetch questions related to subtopics inside this module
    from app.models.module import Subtopic
    if subtopic_id and assessment_type in ("drill", "quiz"):
        subtopic_ids = [subtopic_id]
    else:
        subtopics = db.query(Subtopic).filter(Subtopic.module_id == module_id).all()
        subtopic_ids = [s.id for s in subtopics]
    
    query = db.query(Question).filter(Question.subtopic_id.in_(subtopic_ids))
    if assessment_type:
        query = query.filter(Question.assessment_type == assessment_type)

    if difficulty and assessment_type in ("drill", "quiz"):
        filtered_query = query.filter(Question.difficulty == difficulty)
        questions = filtered_query.all()
        if questions:
            return questions

    questions = query.order_by(Question.id).all()
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
    if not user_id:
        raise HTTPException(status_code=401, detail="Login diperlukan untuk menyimpan jawaban")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    subtopic = _get_question_module(db, question)
    _ensure_assessment_unlocked(
        db=db,
        user_id=user.id,
        module_id=subtopic.module_id,
        assessment_type=question.assessment_type or "quiz",
        subtopic_id=question.subtopic_id if (question.assessment_type or "quiz") in ("drill", "quiz") else None,
    )
        
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
        
    assessment_attempt = _record_assessment_answer(
        db=db,
        user_id=user.id,
        question=question,
        selected_option_id=submission.selected_option_id,
        is_correct=is_correct,
        duration_seconds=submission.duration_seconds,
    )
    learning_update = record_q_learning_update(
        db=db,
        user_id=user.id,
        subtopic_id=question.subtopic_id,
        is_correct=is_correct,
        selected_action=submission.action,
        action_sequence=submission.action_sequence,
        duration_seconds=submission.duration_seconds,
        attempt_accuracy=assessment_attempt.percentage,
        assessment_type=question.assessment_type or "quiz",
    )
    _upsert_knowledge_state(
        db=db,
        user_id=user.id,
        node_id=question.subtopic_id,
        node_type="subtopic",
        value=learning_update["new_mastery"],
        source=question.assessment_type or submission.action,
    )
    if assessment_attempt.finished_at:
        _upsert_knowledge_state(
            db=db,
            user_id=user.id,
            node_id=assessment_attempt.module_id,
            node_type="module",
            value=assessment_attempt.percentage,
            source=assessment_attempt.assessment_type,
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
