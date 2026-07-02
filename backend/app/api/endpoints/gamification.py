from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.api_schemas import (
    LeaderboardEntry,
    RewardItem,
    RewardRedeemRequest,
    RewardRedeemResponse,
)

router = APIRouter()

REWARD_CATALOG = [
    {
        "id": "badge-focus-starter",
        "title": "Badge Focus Starter",
        "description": "Badge profil untuk mahasiswa yang mulai konsisten latihan.",
        "cost": 50,
        "type": "badge",
    },
    {
        "id": "theme-ocean",
        "title": "Tema Ocean",
        "description": "Unlock tema visual biru untuk tampilan belajar.",
        "cost": 120,
        "type": "theme",
    },
    {
        "id": "hint-token-3",
        "title": "3 Hint Token",
        "description": "Token bantuan untuk latihan soal berikutnya.",
        "cost": 90,
        "type": "perk",
    },
]


@router.get("/leaderboard", response_model=list[LeaderboardEntry])
def leaderboard(db: Session = Depends(get_db)):
    users = (
        db.query(User)
        .filter(User.role == "student")
        .order_by(User.xp.desc(), User.total_score.desc(), User.current_streak.desc())
        .limit(20)
        .all()
    )
    return [
        LeaderboardEntry(
            rank=index + 1,
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
        raise HTTPException(status_code=404, detail="Reward tidak ditemukan")

    redeemed_rewards = list(current_user.redeemed_rewards or [])
    if reward["id"] in redeemed_rewards:
        raise HTTPException(status_code=409, detail="Reward sudah pernah ditukar")

    if (current_user.reward_points or 0) < reward["cost"]:
        raise HTTPException(status_code=400, detail="Poin reward belum cukup")

    current_user.reward_points -= reward["cost"]
    redeemed_rewards.append(reward["id"])
    current_user.redeemed_rewards = redeemed_rewards
    db.commit()
    db.refresh(current_user)

    return RewardRedeemResponse(
        success=True,
        message=f"{reward['title']} berhasil ditukar",
        reward_points=current_user.reward_points,
        redeemed_rewards=redeemed_rewards,
        user=current_user,
    )
