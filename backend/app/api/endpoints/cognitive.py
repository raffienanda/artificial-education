from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.cognitive import CognitiveItem, CognitiveProfile, CognitiveResponse
from app.models.user import User
from app.schemas.api_schemas import (
    CognitiveItemResponse,
    CognitiveAnswerInput,
    CognitiveProfileResponse,
    CognitiveSubmitRequest,
)

router = APIRouter()


def _build_profile(db: Session, user_id: int) -> CognitiveProfile:
    responses = (
        db.query(CognitiveResponse, CognitiveItem.stage)
        .join(CognitiveItem, CognitiveResponse.item_id == CognitiveItem.id)
        .filter(CognitiveResponse.user_id == user_id)
        .all()
    )
    stage_scores = {
        "dualism": [],
        "multiplicity": [],
        "relativism": [],
        "commitment": [],
    }

    for response, stage in responses:
        if stage in stage_scores:
            stage_scores[stage].append(response.score)

    averages = {
        stage: round(sum(scores) / len(scores), 2) if scores else 0.0
        for stage, scores in stage_scores.items()
    }
    dominant_stage = max(averages, key=lambda stage: averages[stage])

    profile = db.query(CognitiveProfile).filter(CognitiveProfile.user_id == user_id).first()
    if not profile:
        profile = CognitiveProfile(user_id=user_id)
        db.add(profile)

    profile.dualism_score = averages["dualism"]
    profile.multiplicity_score = averages["multiplicity"]
    profile.relativism_score = averages["relativism"]
    profile.commitment_score = averages["commitment"]
    profile.dominant_stage = dominant_stage
    db.flush()
    return profile


@router.get("/items", response_model=list[CognitiveItemResponse])
def list_items(db: Session = Depends(get_db)):
    return db.query(CognitiveItem).order_by(CognitiveItem.id).all()


@router.get("/profile", response_model=CognitiveProfileResponse)
def get_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    profile = db.query(CognitiveProfile).filter(CognitiveProfile.user_id == current_user.id).first()
    if not profile:
        profile = _build_profile(db=db, user_id=current_user.id)
        db.commit()
        db.refresh(profile)
    return profile


@router.get("/responses", response_model=list[CognitiveAnswerInput])
def get_responses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    responses = db.query(CognitiveResponse).filter(
        CognitiveResponse.user_id == current_user.id,
    ).order_by(CognitiveResponse.item_id).all()
    return [
        CognitiveAnswerInput(item_id=response.item_id, score=response.score)
        for response in responses
    ]


@router.post("/responses", response_model=CognitiveProfileResponse)
def submit_responses(
    payload: CognitiveSubmitRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    existing_response = db.query(CognitiveResponse).filter(
        CognitiveResponse.user_id == current_user.id,
    ).first()
    if existing_response:
        raise HTTPException(status_code=409, detail="Profil kognitif sudah pernah diisi dan tidak bisa diubah")

    item_ids = [answer.item_id for answer in payload.responses]
    existing_items = {
        item.id
        for item in db.query(CognitiveItem).filter(CognitiveItem.id.in_(item_ids)).all()
    }

    for answer in payload.responses:
        if answer.item_id not in existing_items:
            raise HTTPException(status_code=404, detail=f"Item {answer.item_id} tidak ditemukan")
        if answer.score < 1 or answer.score > 5:
            raise HTTPException(status_code=400, detail="Skor harus berada pada rentang 1 sampai 5")

        response = CognitiveResponse(
            user_id=current_user.id,
            item_id=answer.item_id,
            score=answer.score,
        )
        db.add(response)

    db.flush()
    profile = _build_profile(db=db, user_id=current_user.id)
    db.commit()
    db.refresh(profile)
    return profile
