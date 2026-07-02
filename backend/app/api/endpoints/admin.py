from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import uuid4

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.learning_path import InteractionLog, QValue, TopicPrerequisite
from app.models.module import Module
from app.models.question import Question
from app.models.module import Subtopic
from app.models.progress import UserProgress
from app.models.user import User
from app.schemas.api_schemas import (
    AdminQuestionCreate,
    AdminQuestionResponse,
    AdminQuestionUpdate,
    AdminSubtopicCreate,
    AdminSubtopicResponse,
    AdminSubtopicUpdate,
    PrerequisiteCreate,
    PrerequisiteResponse,
    PrerequisiteUpdate,
)

router = APIRouter()


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user


@router.get("/prerequisites", response_model=List[PrerequisiteResponse])
def list_prerequisites(
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    return db.query(TopicPrerequisite).order_by(TopicPrerequisite.topic_id).all()


@router.post("/prerequisites", response_model=PrerequisiteResponse)
def create_prerequisite(
    payload: PrerequisiteCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    if payload.topic_id == payload.prerequisite_id:
        raise HTTPException(status_code=400, detail="Topik tidak boleh menjadi prasyarat dirinya sendiri")

    topic = db.query(Module).filter(Module.id == payload.topic_id).first()
    prerequisite = db.query(Module).filter(Module.id == payload.prerequisite_id).first()
    if not topic or not prerequisite:
        raise HTTPException(status_code=404, detail="Topik atau prasyarat tidak ditemukan")

    existing = db.query(TopicPrerequisite).filter(
        TopicPrerequisite.topic_id == payload.topic_id,
        TopicPrerequisite.prerequisite_id == payload.prerequisite_id,
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail="Relasi prasyarat sudah ada")

    relation = TopicPrerequisite(
        topic_id=payload.topic_id,
        prerequisite_id=payload.prerequisite_id,
        mastery_threshold=payload.mastery_threshold,
    )
    db.add(relation)
    db.commit()
    db.refresh(relation)
    return relation


@router.patch("/prerequisites/{relation_id}", response_model=PrerequisiteResponse)
def update_prerequisite(
    relation_id: int,
    payload: PrerequisiteUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    relation = db.query(TopicPrerequisite).filter(TopicPrerequisite.id == relation_id).first()
    if not relation:
        raise HTTPException(status_code=404, detail="Relasi prasyarat tidak ditemukan")

    relation.mastery_threshold = payload.mastery_threshold
    db.commit()
    db.refresh(relation)
    return relation


@router.delete("/prerequisites/{relation_id}")
def delete_prerequisite(
    relation_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    relation = db.query(TopicPrerequisite).filter(TopicPrerequisite.id == relation_id).first()
    if not relation:
        raise HTTPException(status_code=404, detail="Relasi prasyarat tidak ditemukan")

    db.delete(relation)
    db.commit()
    return {"deleted": True}


@router.get("/questions", response_model=List[AdminQuestionResponse])
def list_questions(
    module_id: str | None = None,
    subtopic_id: str | None = None,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    query = db.query(Question)
    if subtopic_id:
        query = query.filter(Question.subtopic_id == subtopic_id)
    elif module_id:
        subtopic_ids = [
            row.id for row in db.query(Subtopic).filter(Subtopic.module_id == module_id).all()
        ]
        query = query.filter(Question.subtopic_id.in_(subtopic_ids))

    return query.order_by(Question.id).all()


@router.post("/questions", response_model=AdminQuestionResponse)
def create_question(
    payload: AdminQuestionCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    subtopic = db.query(Subtopic).filter(Subtopic.id == payload.subtopic_id).first()
    if not subtopic:
        raise HTTPException(status_code=404, detail="Subtopik tidak ditemukan")

    option_ids = {option.id for option in payload.options}
    if payload.correct_answer not in option_ids:
        raise HTTPException(status_code=400, detail="Jawaban benar harus sesuai salah satu option id")

    question = Question(
        id=f"q-{uuid4().hex[:8]}",
        subtopic_id=payload.subtopic_id,
        question_text=payload.question_text,
        options=[option.model_dump() for option in payload.options],
        correct_answer=payload.correct_answer,
        explanation=payload.explanation,
        difficulty=payload.difficulty,
    )
    db.add(question)
    db.commit()
    db.refresh(question)
    return question


@router.patch("/questions/{question_id}", response_model=AdminQuestionResponse)
def update_question(
    question_id: str,
    payload: AdminQuestionUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Soal tidak ditemukan")

    if payload.subtopic_id is not None:
        subtopic = db.query(Subtopic).filter(Subtopic.id == payload.subtopic_id).first()
        if not subtopic:
            raise HTTPException(status_code=404, detail="Subtopik tidak ditemukan")
        question.subtopic_id = payload.subtopic_id

    if payload.question_text is not None:
        question.question_text = payload.question_text
    if payload.options is not None:
        option_ids = {option.id for option in payload.options}
        correct_answer = payload.correct_answer or question.correct_answer
        if correct_answer not in option_ids:
            raise HTTPException(status_code=400, detail="Jawaban benar harus sesuai salah satu option id")
        question.options = [option.model_dump() for option in payload.options]
    if payload.correct_answer is not None:
        option_ids = {option["id"] for option in question.options}
        if payload.correct_answer not in option_ids:
            raise HTTPException(status_code=400, detail="Jawaban benar harus sesuai salah satu option id")
        question.correct_answer = payload.correct_answer
    if payload.explanation is not None:
        question.explanation = payload.explanation
    if payload.difficulty is not None:
        question.difficulty = payload.difficulty

    db.commit()
    db.refresh(question)
    return question


@router.delete("/questions/{question_id}")
def delete_question(
    question_id: str,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Soal tidak ditemukan")

    db.delete(question)
    db.commit()
    return {"deleted": True}


@router.get("/subtopics", response_model=List[AdminSubtopicResponse])
def list_subtopics(
    module_id: str | None = None,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    query = db.query(Subtopic)
    if module_id:
        query = query.filter(Subtopic.module_id == module_id)
    return query.order_by(Subtopic.module_id, Subtopic.id).all()


@router.post("/subtopics", response_model=AdminSubtopicResponse)
def create_subtopic(
    payload: AdminSubtopicCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    module = db.query(Module).filter(Module.id == payload.module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Modul tidak ditemukan")

    subtopic = Subtopic(
        id=f"sub-{uuid4().hex[:8]}",
        module_id=payload.module_id,
        title=payload.title,
        content=payload.content,
    )
    db.add(subtopic)
    db.commit()
    db.refresh(subtopic)
    return subtopic


@router.patch("/subtopics/{subtopic_id}", response_model=AdminSubtopicResponse)
def update_subtopic(
    subtopic_id: str,
    payload: AdminSubtopicUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    subtopic = db.query(Subtopic).filter(Subtopic.id == subtopic_id).first()
    if not subtopic:
        raise HTTPException(status_code=404, detail="Subtopik tidak ditemukan")

    if payload.module_id is not None:
        module = db.query(Module).filter(Module.id == payload.module_id).first()
        if not module:
            raise HTTPException(status_code=404, detail="Modul tidak ditemukan")
        subtopic.module_id = payload.module_id
    if payload.title is not None:
        subtopic.title = payload.title
    if payload.content is not None:
        subtopic.content = payload.content

    db.commit()
    db.refresh(subtopic)
    return subtopic


@router.delete("/subtopics/{subtopic_id}")
def delete_subtopic(
    subtopic_id: str,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    subtopic = db.query(Subtopic).filter(Subtopic.id == subtopic_id).first()
    if not subtopic:
        raise HTTPException(status_code=404, detail="Subtopik tidak ditemukan")

    db.query(InteractionLog).filter(InteractionLog.subtopic_id == subtopic_id).delete()
    db.query(QValue).filter(QValue.subtopic_id == subtopic_id).delete()
    db.query(UserProgress).filter(UserProgress.topic_id == subtopic_id).delete()
    db.query(Question).filter(Question.subtopic_id == subtopic_id).delete()
    db.delete(subtopic)
    db.commit()
    return {"deleted": True}
