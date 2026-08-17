from math import ceil

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.api_schemas import (
    LeaderboardEntry,
    LeaderboardPageResponse,
    RewardItem,
    RewardRedeemRequest,
    RewardRedeemResponse,
)

router = APIRouter()

REWARD_CATALOG = [
    {
        "id": "theme-forest",
        "title": "Tema Forest",
        "description": "Tema hijau yang tenang untuk tampilan belajar.",
        "cost": 80,
        "type": "theme",
    },
    {
        "id": "theme-ocean",
        "title": "Tema Ocean",
        "description": "Tema teal laut yang lebih segar untuk tampilan belajar.",
        "cost": 150,
        "type": "theme",
    },
    {
        "id": "theme-violet",
        "title": "Tema Pink",
        "description": "Tema pink lembut untuk variasi tampilan dashboard.",
        "cost": 220,
        "type": "theme",
    },
]


@router.get("/leaderboard", response_model=LeaderboardPageResponse)
def leaderboard(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=5, ge=1, le=10),
    db: Session = Depends(get_db),
):
    base_query = db.query(User).filter(User.role == "student")
    total = base_query.count()
    users = (
        base_query
        .order_by(User.xp.desc(), User.total_score.desc(), User.current_streak.desc())
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )
    items = [
        LeaderboardEntry(
            rank=(page - 1) * limit + index + 1,
            id=user.id,
            username=user.username,
            display_name=user.display_name,
            xp=user.xp or 0,
            level=user.level,
            total_score=user.total_score or 0,
            reward_points=user.reward_points or 0,
            current_streak=user.current_streak or 0,
        )
        for index, user in enumerate(users)
    ]
    return LeaderboardPageResponse(
        items=items,
        page=page,
        limit=limit,
        total=total,
        total_pages=max(1, ceil(total / limit)) if total else 1,
    )


@router.get("/rewards", response_model=list[RewardItem])
def rewards():
    return REWARD_CATALOG


@router.post("/rewards/redeem", response_model=RewardRedeemResponse)
def redeem_reward(
    payload: RewardRedeemRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    reward = next((item for item in REWARD_CATALOG if item["id"] == payload.reward_id), None)
    if not reward:
        raise HTTPException(status_code=404, detail="Tema tidak ditemukan")

    redeemed_rewards = list(current_user.redeemed_rewards or [])
    if reward["id"] in redeemed_rewards:
        raise HTTPException(status_code=409, detail="Tema sudah pernah dibeli")

    if (current_user.reward_points or 0) < reward["cost"]:
        raise HTTPException(status_code=400, detail="Poin reward belum cukup")

    current_user.reward_points -= reward["cost"]
    redeemed_rewards.append(reward["id"])
    current_user.redeemed_rewards = redeemed_rewards
    db.commit()
    db.refresh(current_user)

    return RewardRedeemResponse(
        success=True,
        message=f"{reward['title']} berhasil dibeli. Tema bisa dipakai lewat pengaturan.",
        reward_points=current_user.reward_points,
        redeemed_rewards=redeemed_rewards,
        user=current_user,
    )
