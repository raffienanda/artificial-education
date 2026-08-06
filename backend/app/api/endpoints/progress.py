from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_optional_current_user
from app.models.assessment import AssessmentAttempt
from app.models.cognitive import CognitiveProfile
from app.models.learning_path import InteractionLog, QValue
from app.models.module import Module, Subtopic
from app.models.progress import UserProgress
from app.models.user import User
from app.schemas.api_schemas import ProgressResponse
from typing import List

router = APIRouter()


COGNITIVE_RECOMMENDATIONS = {
    "dualism": "Gunakan arahan belajar yang lebih terstruktur, contoh konkret, dan latihan bertahap.",
    "multiplicity": "Bandingkan beberapa contoh penyelesaian, lalu pilih alasan yang paling tepat.",
    "relativism": "Perkuat pembelajaran dengan studi kasus dan alasan mengapa sebuah jawaban benar.",
    "commitment": "Gunakan tantangan mandiri dan refleksi singkat setelah menyelesaikan soal.",
}

COGNITIVE_STUDENT_NOTES = {
    "dualism": "Kamu cenderung lebih nyaman dengan arahan yang jelas, contoh langsung, dan langkah belajar yang berurutan.",
    "multiplicity": "Kamu cenderung cocok ketika melihat beberapa contoh atau cara penyelesaian sebelum menarik kesimpulan.",
    "relativism": "Kamu cenderung cocok dengan pembelajaran yang menjelaskan alasan, konteks, dan hubungan antar konsep.",
    "commitment": "Kamu cenderung cocok dengan tantangan mandiri dan refleksi terhadap keputusan belajar yang kamu ambil.",
}


def _latest_attempt(
    db: Session,
    user_id: int,
    module_id: str,
    assessment_type: str,
    subtopic_id: str | None = None,
) -> AssessmentAttempt | None:
    query = db.query(AssessmentAttempt).filter(
        AssessmentAttempt.user_id == user_id,
        AssessmentAttempt.module_id == module_id,
        AssessmentAttempt.assessment_type == assessment_type,
        AssessmentAttempt.finished_at.isnot(None),
    )
    if subtopic_id:
        query = query.filter(AssessmentAttempt.subtopic_id == subtopic_id)
    return query.order_by(AssessmentAttempt.finished_at.desc()).first()


def _diagnosis_category(effort_level: str, outcome_level: str, post_score: float, average_mastery: float) -> tuple[str, str]:
    if post_score >= 70 and average_mastery >= 70:
        return "siap lanjut", "Hasil akhir dan penguasaan materi sudah cukup kuat untuk melanjutkan modul berikutnya."
    if effort_level == "tinggi" and outcome_level == "rendah":
        return "butuh pendampingan", "Aktivitas belajar sudah tinggi, tetapi hasil akhir masih rendah sehingga strategi belajar perlu dibantu."
    if outcome_level == "rendah":
        return "latihan tambahan", "Hasil akhir masih perlu diperkuat dengan latihan tambahan pada materi yang lemah."
    return "review ringan", "Mahasiswa sudah berada di jalur yang cukup baik, tetapi masih perlu review singkat sebelum lanjut."


def _build_personal_pattern(effort_level: str, outcome_level: str) -> str:
    if effort_level == "tinggi" and outcome_level == "rendah":
        return "aktivitas belajar kamu sudah tinggi, tetapi hasilnya belum sebanding. ini biasanya berarti strategi belajar perlu diubah, bukan sekadar menambah durasi belajar."
    if effort_level == "rendah" and outcome_level == "rendah":
        return "hasil belajar masih rendah dan aktivitas belajar juga belum cukup konsisten. fokus utama kamu adalah membangun ritme belajar dulu."
    if effort_level == "tinggi" and outcome_level == "tinggi":
        return "aktivitas belajar dan hasil kamu sudah berjalan searah. strategi yang dipakai saat ini bisa dipertahankan sambil memperkuat materi yang masih lemah."
    if effort_level == "rendah" and outcome_level == "tinggi":
        return "hasil kamu sudah baik meskipun aktivitas belajar belum terlalu banyak. tetap lakukan review singkat supaya pemahaman tidak cepat turun."
    return "pola belajar kamu cukup stabil, tetapi masih ada bagian yang perlu diperkuat sebelum melanjutkan."


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


@router.get("/module-diagnosis/{module_id}")
def get_module_diagnosis(
    module_id: str,
    user_id: int = 1,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_optional_current_user),
):
    user_id = current_user.id if current_user else user_id
    module = db.query(Module).filter(Module.id == module_id).first()
    if not module:
        return {"available": False, "message": "Modul tidak ditemukan."}

    subtopics = sorted(module.subtopics, key=lambda item: item.id)
    subtopic_ids = [item.id for item in subtopics]
    latest_post_test = _latest_attempt(
        db=db,
        user_id=user_id,
        module_id=module_id,
        assessment_type="post_test",
    )
    latest_pre_test = _latest_attempt(
        db=db,
        user_id=user_id,
        module_id=module_id,
        assessment_type="pre_test",
    )

    if not latest_post_test:
        return {
            "available": False,
            "message": "Diagnosis modul tersedia setelah post test selesai.",
        }

    progress_rows = db.query(UserProgress).filter(
        UserProgress.user_id == user_id,
        UserProgress.topic_id.in_(subtopic_ids),
    ).all()
    mastery_by_subtopic = {row.topic_id: row.mastery for row in progress_rows}
    subtopic_masteries = [
        {
            "id": subtopic.id,
            "title": subtopic.title,
            "mastery": round(mastery_by_subtopic.get(subtopic.id, 0.0), 2),
        }
        for subtopic in subtopics
    ]
    weak_subtopics = sorted(
        [item for item in subtopic_masteries if item["mastery"] < 70.0],
        key=lambda item: item["mastery"],
    )[:3]

    average_mastery = (
        sum(item["mastery"] for item in subtopic_masteries) / len(subtopic_masteries)
        if subtopic_masteries else 0.0
    )
    quiz_attempts = [
        attempt for attempt in (
            _latest_attempt(
                db=db,
                user_id=user_id,
                module_id=module_id,
                assessment_type="quiz",
                subtopic_id=subtopic.id,
            )
            for subtopic in subtopics
        )
        if attempt
    ]
    quiz_average = (
        sum(attempt.percentage or 0.0 for attempt in quiz_attempts) / len(quiz_attempts)
        if quiz_attempts else 0.0
    )

    logs = db.query(InteractionLog).filter(
        InteractionLog.user_id == user_id,
        InteractionLog.subtopic_id.in_(subtopic_ids),
    ).all()
    total_interactions = len(logs)
    total_minutes = round(sum(log.duration_seconds or 0 for log in logs) / 60, 1)
    effort_score = min(100, round((total_interactions * 8) + (total_minutes * 2)))
    effort_level = "tinggi" if effort_score >= 70 else "sedang" if effort_score >= 35 else "rendah"

    post_score = latest_post_test.percentage or 0.0
    outcome_score = round((post_score * 0.6) + (average_mastery * 0.4), 2)
    outcome_level = "tinggi" if outcome_score >= 70 else "sedang" if outcome_score >= 50 else "rendah"
    category, summary = _diagnosis_category(
        effort_level=effort_level,
        outcome_level=outcome_level,
        post_score=post_score,
        average_mastery=average_mastery,
    )

    action_counts: dict[str, int] = {}
    for log in logs:
        action_counts[log.action] = action_counts.get(log.action, 0) + 1
    most_used_action = max(action_counts, key=action_counts.get) if action_counts else None

    q_rows = db.query(QValue).filter(
        QValue.user_id == user_id,
        QValue.subtopic_id.in_(subtopic_ids),
    ).all()
    q_by_action: dict[str, list[float]] = {}
    for row in q_rows:
        q_by_action.setdefault(row.action, []).append(row.value or 0.0)
    q_action_scores = {
        action: round(sum(values) / len(values), 2)
        for action, values in q_by_action.items()
        if values
    }
    most_effective_action = max(q_action_scores, key=q_action_scores.get) if q_action_scores else None

    profile = db.query(CognitiveProfile).filter(CognitiveProfile.user_id == user_id).first()
    cognitive_stage = profile.dominant_stage if profile else "unknown"
    cognitive_recommendation = COGNITIVE_RECOMMENDATIONS.get(
        cognitive_stage,
        "Profil kognitif belum tersedia, jadi saran masih memakai pola umum dari hasil belajar.",
    )
    cognitive_student_note = COGNITIVE_STUDENT_NOTES.get(
        cognitive_stage,
        "Profil kognitif belum tersedia, jadi saran personal masih memakai pola umum dari hasil belajar.",
    )
    user = db.query(User).filter(User.id == user_id).first()
    learner_name = user.display_name or user.username if user else "mahasiswa"
    personal_pattern = _build_personal_pattern(
        effort_level=effort_level,
        outcome_level=outcome_level,
    )

    recommendations = []
    if weak_subtopics:
        weak_titles = ", ".join(item["title"] for item in weak_subtopics)
        recommendations.append(f"Perkuat ulang materi: {weak_titles}.")
    if effort_level == "tinggi" and outcome_level == "rendah":
        recommendations.append("Jadwalkan belajar tambahan atau pendampingan karena aktivitas tinggi belum sebanding dengan hasil.")
    elif effort_level == "rendah" and outcome_level != "tinggi":
        recommendations.append("Tingkatkan konsistensi belajar sebelum lanjut ke modul berikutnya.")
    if most_effective_action:
        recommendations.append(f"Gunakan strategi yang relatif efektif untuk akun ini: {most_effective_action}.")
    recommendations.append(cognitive_recommendation)

    personal_recommendations = []
    if weak_subtopics:
        personal_recommendations.append(
            f"{learner_name}, fokuskan belajar tambahan pada {weak_subtopics[0]['title']} terlebih dahulu karena bagian ini punya mastery paling rendah."
        )
    if effort_level == "tinggi" and outcome_level == "rendah":
        personal_recommendations.append(
            "Karena kamu sudah cukup aktif tetapi hasilnya belum naik, coba ubah cara belajar: mulai dari contoh konkret, lalu kerjakan latihan bertahap dengan pembahasan."
        )
    elif effort_level == "rendah" and outcome_level != "tinggi":
        personal_recommendations.append(
            "Tambahkan sesi belajar pendek tetapi rutin sebelum mencoba post test lagi."
        )
    elif most_effective_action:
        personal_recommendations.append(
            f"Untuk akun kamu, strategi yang sejauh ini paling membantu adalah {most_effective_action}. gunakan itu sebagai cara belajar utama."
        )
    personal_recommendations.append(cognitive_student_note)

    return {
        "available": True,
        "module_id": module.id,
        "module_title": module.title,
        "learner_name": learner_name,
        "category": category,
        "summary": summary,
        "personal_pattern": personal_pattern,
        "pre_test_score": round(latest_pre_test.percentage or 0.0, 2) if latest_pre_test else None,
        "quiz_average": round(quiz_average, 2),
        "post_test_score": round(post_score, 2),
        "average_mastery": round(average_mastery, 2),
        "effort_score": effort_score,
        "effort_level": effort_level,
        "outcome_score": outcome_score,
        "outcome_level": outcome_level,
        "total_interactions": total_interactions,
        "total_minutes": total_minutes,
        "weak_subtopics": weak_subtopics,
        "most_used_action": most_used_action,
        "most_effective_action": most_effective_action,
        "q_action_scores": q_action_scores,
        "cognitive_stage": cognitive_stage,
        "cognitive_recommendation": cognitive_recommendation,
        "cognitive_student_note": cognitive_student_note,
        "recommendations": recommendations,
        "personal_recommendations": personal_recommendations,
    }
