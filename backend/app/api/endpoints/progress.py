from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_optional_current_user
from app.models.progress import UserProgress
from app.models.user import User
from app.schemas.api_schemas import ProgressResponse
from typing import List

router = APIRouter()

@router.get("/", response_model=List[ProgressResponse])
def get_progress(
    user_id: int = 1,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_optional_current_user),
):
    user_id = current_user.id if current_user else user_id
    progress_list = db.query(UserProgress).filter(UserProgress.user_id == user_id).all()
    return progress_list

@router.get("/overall")
def get_overall_mastery(
    user_id: int = 1,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_optional_current_user),
):
    user_id = current_user.id if current_user else user_id
    user = db.query(User).filter(User.id == user_id).first()
    progress_list = db.query(UserProgress).filter(UserProgress.user_id == user_id).all()
    
    if not progress_list:
        return {"overall": 0, "xp": user.xp if user else 0, "combo": user.combo if user else 0}
        
    total_mastery = sum([p.mastery for p in progress_list])
    overall = total_mastery / len(progress_list)
    
    return {"overall": round(overall), "xp": user.xp, "combo": user.combo}
