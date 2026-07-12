from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_optional_current_user
from app.models.assessment import AssessmentAttempt
from app.models.learning_path import InteractionLog
from app.models.module import Module, Subtopic
from app.models.progress import UserProgress
from app.models.user import User
from app.schemas.api_schemas import ProgressResponse
from typing import List

router = APIRouter()


@router.get("/gates")
def get_learning_gates(
    user_id: int = 1,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_optional_current_user),
):
    """Return assessment completion gates used by module/subtopic locking."""
    user_id = current_user.id if current_user else user_id
    modules = db.query(Module).order_by(Module.order).all()
    attempts = db.query(AssessmentAttempt).filter(
        AssessmentAttempt.user_id == user_id,
        AssessmentAttempt.assessment_type.in_(["pre_test", "quiz", "post_test"]),
        AssessmentAttempt.finished_at.isnot(None),
    ).all()
    progress_rows = db.query(UserProgress).filter(UserProgress.user_id == user_id).all()

    mastery_by_topic = {row.topic_id: row.mastery for row in progress_rows}
    completed_pretests = {}
    completed_posttests = {}
    completed_subtopic_quizzes = {}
    passed_modules = {}

    raw_completed_subtopic_quizzes = {}

    for attempt in attempts:
        if attempt.assessment_type == "pre_test":
            completed_pretests[attempt.module_id] = True
        elif attempt.assessment_type == "post_test" and attempt.passed:
            completed_posttests[attempt.module_id] = True
        elif attempt.assessment_type == "quiz" and attempt.subtopic_id and attempt.passed:
            raw_completed_subtopic_quizzes[f"{attempt.module_id}:{attempt.subtopic_id}"] = True

    for module in modules:
        for subtopic in sorted(module.subtopics, key=lambda item: item.id):
            key = f"{module.id}:{subtopic.id}"
            if not raw_completed_subtopic_quizzes.get(key):
                break
            completed_subtopic_quizzes[key] = True

    for module in modules:
        subtopic_ids = [subtopic.id for subtopic in module.subtopics]
        if not subtopic_ids:
            passed_modules[module.id] = False
            continue
        average_mastery = sum(mastery_by_topic.get(subtopic_id, 0.0) for subtopic_id in subtopic_ids) / len(subtopic_ids)
        passed_modules[module.id] = bool(completed_posttests.get(module.id)) and average_mastery >= 60.0

    return {
        "completed_pretests": completed_pretests,
        "completed_posttests": completed_posttests,
        "completed_subtopic_quizzes": completed_subtopic_quizzes,
        "passed_modules": passed_modules,
    }


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


@router.get("/history")
def get_learning_history(
    user_id: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_optional_current_user),
):
    """Return recent learning activities for a user, derived from InteractionLog."""
    user_id = current_user.id if current_user else user_id

    logs = (
        db.query(InteractionLog, Subtopic.title)
        .join(Subtopic, InteractionLog.subtopic_id == Subtopic.id)
        .filter(InteractionLog.user_id == user_id)
        .order_by(InteractionLog.created_at.desc())
        .limit(limit)
        .all()
    )

    activities = []
    for log, subtopic_title in logs:
        # Determine mastery-based color and icon
        score_pct = log.score * 100 if log.score <= 1 else log.score
        if score_pct >= 70:
            color = "success"
            icon = "📗"
        elif score_pct >= 40:
            color = "primary"
            icon = "📘"
        else:
            color = "warning"
            icon = "📙"

        # Format time as relative string
        now = datetime.now(timezone.utc)
        created = log.created_at.replace(tzinfo=timezone.utc) if log.created_at.tzinfo is None else log.created_at
        diff = now - created
        if diff.days == 0:
            time_str = f"Hari ini, {created.strftime('%H:%M')}"
        elif diff.days == 1:
            time_str = f"Kemarin, {created.strftime('%H:%M')}"
        else:
            time_str = f"{diff.days} hari lalu, {created.strftime('%H:%M')}"

        activities.append({
            "id": f"act-{log.id}",
            "title": subtopic_title,
            "time": time_str,
            "mastery": round(score_pct),
            "icon": icon,
            "color": color,
        })

    return activities


@router.get("/weekly")
def get_weekly_progress(
    user_id: int = 1,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_optional_current_user),
):
    """Return study minutes aggregated by day of the week for the current week."""
    user_id = current_user.id if current_user else user_id

    # Calculate Monday of current week
    now = datetime.now(timezone.utc)
    monday = (now - timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)

    logs = (
        db.query(InteractionLog)
        .filter(
            InteractionLog.user_id == user_id,
            InteractionLog.created_at >= monday,
        )
        .all()
    )

    # Aggregate duration per day index (0=Mon, 6=Sun)
    day_names = ["Sen", "Sel", "Rab", "Kam", "Jum", "Sab", "Min"]
    day_totals = {i: 0 for i in range(7)}

    for log in logs:
        created = log.created_at.replace(tzinfo=timezone.utc) if log.created_at.tzinfo is None else log.created_at
        day_index = created.weekday()
        day_totals[day_index] += log.duration_seconds or 0

    weekly = [
        {"day": day_names[i], "minutes": round(day_totals[i] / 60)}
        for i in range(7)
    ]

    return weekly


@router.get("/status-message")
def get_status_message(
    user_id: int = 1,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_optional_current_user),
):
    """Generate a dynamic status message based on actual user mastery data."""
    user_id = current_user.id if current_user else user_id

    progress_list = db.query(UserProgress).filter(UserProgress.user_id == user_id).all()

    if not progress_list:
        return {"statusMessage": "Mulai belajar untuk melihat progress kamu!"}

    weak_count = sum(1 for p in progress_list if p.mastery < 70)
    mastered_count = sum(1 for p in progress_list if p.mastery >= 90)
    total = len(progress_list)
    overall = sum(p.mastery for p in progress_list) / total

    if overall >= 90:
        message = f"Luar biasa! Kamu menguasai {mastered_count} dari {total} materi. Pertahankan!"
    elif overall >= 70:
        message = f"Bagus! Tinggal {weak_count} materi yang perlu diperkuat lagi."
    elif overall >= 50:
        message = f"Kamu perlu fokus pada {weak_count} materi yang belum dikuasai."
    else:
        message = f"Ada {weak_count} materi yang membutuhkan perhatian lebih. Semangat!"

    return {"statusMessage": message}
