from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import create_access_token, get_current_user, hash_password, verify_password
from app.models.user import User
from app.models.module import Subtopic
from app.models.progress import UserProgress
from app.schemas.api_schemas import AuthLogin, AuthRegister, AuthToken, UserResponse

router = APIRouter()


@router.post("/register", response_model=AuthToken)
def register(payload: AuthRegister, db: Session = Depends(get_db)):
    username = payload.username.strip().lower()
    if len(username) < 3:
        raise HTTPException(status_code=400, detail="Username minimal 3 karakter")
    if len(payload.password) < 6:
        raise HTTPException(status_code=400, detail="Password minimal 6 karakter")

    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="Username sudah digunakan")

    user = User(
        username=username,
        display_name=payload.display_name or username,
        password_hash=hash_password(payload.password),
        role="student",
        xp=0,
        combo=0,
        total_score=0,
        reward_points=0,
        current_streak=0,
        longest_streak=0,
        redeemed_rewards=[],
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    subtopics = db.query(Subtopic).all()
    for subtopic in subtopics:
        db.add(UserProgress(
            user_id=user.id,
            topic_id=subtopic.id,
            mastery=0.0,
            status="learning",
            p_known=0.0,
            p_learn=0.2,
            p_guess=0.25,
            p_slip=0.1,
        ))
    db.commit()

    return AuthToken(access_token=create_access_token(user), user=user)


@router.post("/login", response_model=AuthToken)
def login(payload: AuthLogin, db: Session = Depends(get_db)):
    username = payload.username.strip().lower()
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username atau password salah",
        )

    return AuthToken(access_token=create_access_token(user), user=user)


@router.get("/me", response_model=UserResponse)
def me(current_user: User = Depends(get_current_user)):
    return current_user
