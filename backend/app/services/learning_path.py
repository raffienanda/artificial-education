from sqlalchemy.orm import Session

from app.ml.gkt import gkt_model
from app.ml.q_learning import q_agent
from app.models.learning_path import InteractionLog, QValue, TopicPrerequisite
from app.models.module import Module, Subtopic
from app.models.progress import UserProgress


def get_or_create_q_value(
    db: Session,
    user_id: int,
    subtopic_id: str,
    state: str,
    action: str,
) -> QValue:
    q_value = db.query(QValue).filter(
        QValue.user_id == user_id,
        QValue.subtopic_id == subtopic_id,
        QValue.state == state,
        QValue.action == action,
    ).first()

    if q_value:
        return q_value

    q_value = QValue(
        user_id=user_id,
        subtopic_id=subtopic_id,
        state=state,
        action=action,
        value=0.0,
    )
    db.add(q_value)
    db.flush()
    return q_value


def get_q_values_for_state(db: Session, user_id: int, subtopic_id: str, state: str) -> dict[str, float]:
    rows = db.query(QValue).filter(
        QValue.user_id == user_id,
        QValue.subtopic_id == subtopic_id,
        QValue.state == state,
    ).all()
    return {row.action: row.value for row in rows}


def get_progress_mastery(db: Session, user_id: int, topic_id: str) -> float:
    progress = db.query(UserProgress).filter(
        UserProgress.user_id == user_id,
        UserProgress.topic_id == topic_id,
    ).first()
    return progress.mastery if progress else 0.0


def get_recent_failures(db: Session, user_id: int, subtopic_id: str) -> int:
    logs = db.query(InteractionLog).filter(
        InteractionLog.user_id == user_id,
        InteractionLog.subtopic_id == subtopic_id,
    ).order_by(InteractionLog.created_at.desc()).limit(3).all()

    failures = 0
    for log in logs:
        if log.reward >= 0:
            break
        failures += 1
    return failures


def get_or_create_progress(db: Session, user_id: int, topic_id: str) -> UserProgress:
    progress = db.query(UserProgress).filter(
        UserProgress.user_id == user_id,
        UserProgress.topic_id == topic_id,
    ).first()

    if progress:
        return progress

    progress = UserProgress(user_id=user_id, topic_id=topic_id, mastery=0.0, status="learning")
    db.add(progress)
    db.flush()
    return progress


def update_progress_from_answer(db: Session, user_id: int, subtopic_id: str, is_correct: bool) -> tuple[UserProgress, float]:
    progress = get_or_create_progress(db, user_id=user_id, topic_id=subtopic_id)
    mastery_before = progress.mastery

    if is_correct:
        progress.mastery = min(100.0, progress.mastery + 10.0)
    else:
        progress.mastery = max(0.0, progress.mastery - 5.0)

    progress.p_known = progress.mastery / 100.0
    if progress.mastery >= 80.0:
        progress.status = "proficient"
    elif progress.mastery <= 30.0:
        progress.status = "needs-review"
    else:
        progress.status = "learning"

    return progress, mastery_before


def record_q_learning_update(
    db: Session,
    user_id: int,
    subtopic_id: str,
    is_correct: bool,
    selected_action: str = "easy_quiz",
    duration_seconds: int = 0,
) -> dict:
    mastery_before = get_progress_mastery(db, user_id=user_id, topic_id=subtopic_id)
    failures_before = get_recent_failures(db, user_id=user_id, subtopic_id=subtopic_id)
    state = q_agent.build_state(mastery=mastery_before, recent_failures=failures_before)

    progress, mastery_before = update_progress_from_answer(
        db=db,
        user_id=user_id,
        subtopic_id=subtopic_id,
        is_correct=is_correct,
    )

    failures_after = 0 if is_correct else failures_before + 1
    next_state = q_agent.build_state(mastery=progress.mastery, recent_failures=failures_after)
    next_q_values = get_q_values_for_state(
        db=db,
        user_id=user_id,
        subtopic_id=subtopic_id,
        state=next_state,
    )
    next_max_q = max(next_q_values.values(), default=0.0)

    q_value = get_or_create_q_value(
        db=db,
        user_id=user_id,
        subtopic_id=subtopic_id,
        state=state,
        action=selected_action,
    )

    reward = q_agent.calculate_reward(
        is_correct=is_correct,
        mastery_before=mastery_before,
        mastery_after=progress.mastery,
        first_attempt=failures_before == 0,
    )
    q_value.value = q_agent.update_q_value(
        current_q=q_value.value,
        reward=reward,
        next_max_q=next_max_q,
    )

    db.add(InteractionLog(
        user_id=user_id,
        subtopic_id=subtopic_id,
        state=state,
        action=selected_action,
        reward=reward,
        score=1.0 if is_correct else 0.0,
        duration_seconds=duration_seconds,
    ))

    return {
        "reward": reward,
        "new_mastery": progress.mastery,
        "state": state,
        "next_state": next_state,
        "action": selected_action,
        "q_value": q_value.value,
    }


def build_topic_mastery(db: Session, user_id: int) -> dict[str, float]:
    modules = db.query(Module).all()
    topic_mastery = {}

    for module in modules:
        subtopic_ids = [subtopic.id for subtopic in module.subtopics]
        if not subtopic_ids:
            topic_mastery[module.id] = 0.0
            continue

        progress_rows = db.query(UserProgress).filter(
            UserProgress.user_id == user_id,
            UserProgress.topic_id.in_(subtopic_ids),
        ).all()
        progress_by_topic = {progress.topic_id: progress.mastery for progress in progress_rows}
        total_mastery = sum(progress_by_topic.get(subtopic_id, 0.0) for subtopic_id in subtopic_ids)
        topic_mastery[module.id] = total_mastery / len(subtopic_ids)

    return topic_mastery


def build_prerequisite_graph(db: Session) -> dict[str, list[dict]]:
    rows = db.query(TopicPrerequisite).all()
    graph: dict[str, list[dict]] = {}

    for row in rows:
        graph.setdefault(row.topic_id, []).append({
            "id": row.prerequisite_id,
            "mastery_threshold": row.mastery_threshold or 60.0,
        })

    if graph:
        return graph

    modules = db.query(Module).order_by(Module.order).all()
    return {
        modules[index].id: [{
            "id": modules[index - 1].id,
            "mastery_threshold": 60.0,
        }]
        for index in range(1, len(modules))
    }


def recommend_next_step(db: Session, user_id: int, current_module_id: str, current_subtopic_id: str) -> dict:
    current_subtopic = db.query(Subtopic).filter(Subtopic.id == current_subtopic_id).first()
    if not current_subtopic:
        return {
            "macro_action": "continue",
            "recommended_module_id": current_module_id,
            "recommended_subtopic_id": current_subtopic_id,
            "micro_action": "show_text",
            "reason": "Subtopik belum ditemukan, gunakan materi teks sebagai fallback.",
        }

    topic_mastery = build_topic_mastery(db=db, user_id=user_id)
    prerequisite_graph = build_prerequisite_graph(db=db)
    macro = gkt_model.evaluate_mastery(
        current_topic_id=current_module_id,
        topic_mastery=topic_mastery,
        prerequisites=prerequisite_graph,
    )

    recommended_module_id = macro["recommended_topic"]
    recommended_subtopic_id = current_subtopic_id

    if recommended_module_id != current_module_id:
        recommended_subtopic = db.query(Subtopic).filter(
            Subtopic.module_id == recommended_module_id,
        ).order_by(Subtopic.id).first()
        if recommended_subtopic:
            recommended_subtopic_id = recommended_subtopic.id

    mastery = get_progress_mastery(db=db, user_id=user_id, topic_id=recommended_subtopic_id)
    failures = get_recent_failures(db=db, user_id=user_id, subtopic_id=recommended_subtopic_id)
    state = q_agent.build_state(mastery=mastery, recent_failures=failures)
    q_values = get_q_values_for_state(
        db=db,
        user_id=user_id,
        subtopic_id=recommended_subtopic_id,
        state=state,
    )
    action = q_agent.select_action(q_values)

    return {
        "macro_action": macro["action"],
        "recommended_module_id": recommended_module_id,
        "recommended_subtopic_id": recommended_subtopic_id,
        "micro_action": action,
        "state": state,
        "q_values": q_values,
        "reason": macro["reason"],
    }
