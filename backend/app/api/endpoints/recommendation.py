from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_optional_current_user
from app.models.learning_path import InteractionLog
from app.models.user import User
from app.schemas.api_schemas import InteractionLogResponse, RecommendationRequest, RecommendationResponse
from app.services.learning_path import recommend_next_step
from typing import List

router = APIRouter()


@router.post("/next", response_model=RecommendationResponse)
def get_next_recommendation(
    payload: RecommendationRequest,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_optional_current_user),
):
    user_id = current_user.id if current_user else payload.user_id
    return recommend_next_step(
        db=db,
        user_id=user_id,
        current_module_id=payload.current_module_id,
        current_subtopic_id=payload.current_subtopic_id,
    )


@router.get("/logs", response_model=List[InteractionLogResponse])
def get_interaction_logs(
    user_id: int = 1,
    limit: int = 8,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_optional_current_user),
):
    user_id = current_user.id if current_user else user_id
    return db.query(InteractionLog).filter(
        InteractionLog.user_id == user_id,
    ).order_by(
        InteractionLog.created_at.desc()
    ).limit(limit).all()
