from sqlalchemy.orm import Session

from app.ml.neural_gkt import load_neural_gkt_model
from app.ml.gkt import gkt_model
from app.models.assessment import AssessmentAttempt
from app.ml.q_learning import q_agent
from app.models.cognitive import CognitiveProfile
from app.models.learning_path import InteractionLog, QValue, TopicPrerequisite
from app.models.module import Module, Subtopic
from app.models.progress import UserProgress

# Bagian policy profil kognitif untuk membatasi/mengarahkan action q-learning.
COGNITIVE_ACTION_POLICY = {
    # Profil kognitif membatasi urutan prioritas action agar rekomendasi lebih personal.
    "dualism": ("show_text", "easy_quiz", "show_video", "review_previous"),
    "multiplicity": ("show_video", "easy_quiz", "show_text", "hard_quiz"),
    "relativism": ("easy_quiz", "hard_quiz", "show_video", "show_text"),
    "commitment": ("hard_quiz", "easy_quiz", "show_text", "show_video"),
}

COGNITIVE_STRATEGIES = {
    "dualism": "Berikan instruksi lebih terstruktur, contoh konkret, dan quiz bertahap.",
    "multiplicity": "Arahkan mahasiswa membandingkan beberapa cara berpikir sambil tetap diberi batasan yang jelas.",
    "relativism": "Dorong analisis berbasis alasan, fakta, dan konteks sebelum memilih jawaban.",
    "commitment": "Berikan tantangan yang menuntut keputusan mandiri dan pertanggungjawaban argumen.",
}


# Bagian membaca profil kognitif mahasiswa dari database.
def get_cognitive_stage(db: Session, user_id: int) -> str:
    profile = db.query(CognitiveProfile).filter(CognitiveProfile.user_id == user_id).first()
    if not profile:
        return "unknown"

    has_scores = any([
        profile.dualism_score,
        profile.multiplicity_score,
        profile.relativism_score,
        profile.commitment_score,
    ])
    if not has_scores:
        return "unknown"

    return profile.dominant_stage or "unknown"


# Bagian menggabungkan state q-learning dengan profil kognitif.
def build_cognitive_state(base_state: str, cognitive_stage: str) -> str:
    # State q-learning diperluas dengan profil kognitif, misalnya "medium:stable:dualism".
    if cognitive_stage == "unknown":
        return base_state
    return f"{base_state}:{cognitive_stage}"


# Bagian menentukan action yang boleh dipakai sesuai profil kognitif.
def get_allowed_actions_for_stage(cognitive_stage: str) -> tuple[str, ...]:
    return COGNITIVE_ACTION_POLICY.get(cognitive_stage, q_agent.ACTIONS)


# Bagian teks strategi belajar berdasarkan profil kognitif.
def get_strategy_for_stage(cognitive_stage: str) -> str:
    return COGNITIVE_STRATEGIES.get(
        cognitive_stage,
        "Profil kognitif belum diisi, jadi rekomendasi masih memakai pola umum dari mastery dan riwayat jawaban.",
    )


# Bagian pengecekan apakah q-value sudah punya pengalaman belajar.
def has_learned_action_values(q_values: dict[str, float], allowed_actions: tuple[str, ...]) -> bool:
    return any(abs(q_values.get(action, 0.0)) > 0.0001 for action in allowed_actions)


# Bagian pengecekan apakah mahasiswa bisa direkomendasikan review subtopik sebelumnya.
def can_review_previous_subtopic(db: Session, subtopic_id: str) -> bool:
    subtopic = db.query(Subtopic).filter(Subtopic.id == subtopic_id).first()
    if not subtopic:
        return False

    module_subtopics = db.query(Subtopic).filter(
        Subtopic.module_id == subtopic.module_id,
    ).order_by(Subtopic.id).all()
    subtopic_ids = [item.id for item in module_subtopics]
    return subtopic_id in subtopic_ids and subtopic_ids.index(subtopic_id) > 0


# Bagian cold start sebelum q-learning punya q-value yang cukup.
def select_cold_start_action(mastery: float, failures: int, cognitive_stage: str, can_review_previous: bool = True) -> str:
    # Cold start dipakai sebelum q-value punya pengalaman yang cukup untuk memilih action.
    if failures >= 2:
        return "review_previous" if can_review_previous else "show_text"

    if mastery < 30:
        if cognitive_stage == "multiplicity":
            return "show_video"
        return "show_text"

    if mastery < 55:
        return "easy_quiz"

    if mastery < 80:
        if cognitive_stage in ("relativism", "commitment"):
            return "hard_quiz"
        return "easy_quiz"

    return "hard_quiz"


# Bagian mengambil atau membuat q-value di database.
def get_or_create_q_value(
    db: Session,
    user_id: int,
    subtopic_id: str,
    state: str,
    action: str,
) -> QValue:
    # Q-value disimpan per mahasiswa, subtopik, state, dan action.
    # Jadi pengalaman belajar tiap akun tidak bercampur dengan akun lain.
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


# Bagian mengambil q-value pada satu state tertentu.
def get_q_values_for_state(db: Session, user_id: int, subtopic_id: str, state: str) -> dict[str, float]:
    rows = db.query(QValue).filter(
        QValue.user_id == user_id,
        QValue.subtopic_id == subtopic_id,
        QValue.state == state,
    ).all()
    return {row.action: row.value for row in rows}


# Bagian mengambil semua q-value subtopik untuk kebutuhan debug/demo.
def get_q_values_for_subtopic(db: Session, user_id: int, subtopic_id: str) -> dict[str, dict[str, float]]:
    rows = db.query(QValue).filter(
        QValue.user_id == user_id,
        QValue.subtopic_id == subtopic_id,
    ).order_by(QValue.state, QValue.action).all()

    grouped: dict[str, dict[str, float]] = {}
    for row in rows:
        grouped.setdefault(row.state, {})[row.action] = row.value
    return grouped


# Bagian membaca mastery subtopik mahasiswa.
def get_progress_mastery(db: Session, user_id: int, topic_id: str) -> float:
    progress = db.query(UserProgress).filter(
        UserProgress.user_id == user_id,
        UserProgress.topic_id == topic_id,
    ).first()
    return progress.mastery if progress else 0.0


# Bagian menghitung kegagalan terbaru sebagai komponen state q-learning.
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


# Bagian mengambil atau membuat progress mastery subtopik.
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


# Bagian konfigurasi perubahan mastery per jenis assessment.
MASTERY_DELTAS = {
    # Delta ini menaikkan/menurunkan mastery subtopik setiap jawaban masuk.
    # Nilai formal assessment dibuat lebih besar daripada drill karena bobotnya lebih penting.
    "pre_test": (8.0, -3.0),
    "quiz": (18.0, -8.0),
    "post_test": (20.0, -10.0),
    "drill": (6.0, -4.0),
}


# Bagian update mastery setelah jawaban mahasiswa masuk.
def update_progress_from_answer(
    db: Session,
    user_id: int,
    subtopic_id: str,
    is_correct: bool,
    assessment_type: str = "quiz",
) -> tuple[UserProgress, float]:
    progress = get_or_create_progress(db, user_id=user_id, topic_id=subtopic_id)
    mastery_before = progress.mastery
    correct_delta, wrong_delta = MASTERY_DELTAS.get(assessment_type, MASTERY_DELTAS["quiz"])

    if is_correct:
        progress.mastery = min(100.0, progress.mastery + correct_delta)
    else:
        progress.mastery = max(0.0, progress.mastery + wrong_delta)

    progress.p_known = progress.mastery / 100.0
    if progress.mastery >= 80.0:
        progress.status = "proficient"
    elif progress.mastery <= 30.0:
        progress.status = "needs-review"
    else:
        progress.status = "learning"

    return progress, mastery_before


# Bagian menyusun urutan action belajar yang akan diberi kredit reward.
def normalize_action_sequence(
    action_sequence: list[str] | None,
    selected_action: str,
    assessment_type: str,
) -> list[str]:
    # Untuk quiz, sistem bisa memberi kredit ke beberapa action yang sempat dipakai
    # sebelum menjawab soal, misalnya ringkasan lalu video lalu quiz.
    raw_actions = action_sequence or []
    if assessment_type != "quiz":
        raw_actions = [assessment_type]
    elif selected_action and selected_action not in raw_actions:
        raw_actions = [*raw_actions, selected_action]

    actions: list[str] = []
    for action in raw_actions:
        if not action:
            continue
        if actions and actions[-1] == action:
            continue
        actions.append(action)

    return actions or [selected_action or assessment_type]


# Bagian pembagian kredit reward ke action yang dipakai sebelum quiz.
def build_action_credits(actions: list[str]) -> dict[str, float]:
    # Action terakhir mendapat kredit terbesar karena paling dekat dengan jawaban mahasiswa.
    credits: dict[str, float] = {}
    total = len(actions)
    for index, action in enumerate(actions):
        distance_from_last = total - index - 1
        if distance_from_last == 0:
            credit = 1.0
        elif distance_from_last == 1:
            credit = 0.6
        else:
            credit = 0.4
        credits[action] = max(credits.get(action, 0.0), credit)
    return credits


# Bagian utama update q-learning dan q-value.
def record_q_learning_update(
    db: Session,
    user_id: int,
    subtopic_id: str,
    is_correct: bool,
    selected_action: str = "easy_quiz",
    action_sequence: list[str] | None = None,
    duration_seconds: int = 0,
    attempt_accuracy: float | None = None,
    assessment_type: str = "quiz",
) -> dict:
    # Alur utama q-learning:
    # 1. bentuk state dari mastery, kegagalan, dan profil kognitif
    # 2. update mastery dari jawaban
    # 3. hitung reward
    # 4. update q-value tiap action dengan persamaan Bellman
    cognitive_stage = get_cognitive_stage(db=db, user_id=user_id)
    mastery_before = get_progress_mastery(db, user_id=user_id, topic_id=subtopic_id)
    failures_before = get_recent_failures(db, user_id=user_id, subtopic_id=subtopic_id)
    base_state = q_agent.build_state(mastery=mastery_before, recent_failures=failures_before)
    state = build_cognitive_state(base_state=base_state, cognitive_stage=cognitive_stage)

    progress, mastery_before = update_progress_from_answer(
        db=db,
        user_id=user_id,
        subtopic_id=subtopic_id,
        is_correct=is_correct,
        assessment_type=assessment_type,
    )

    failures_after = 0 if is_correct else failures_before + 1
    next_base_state = q_agent.build_state(mastery=progress.mastery, recent_failures=failures_after)
    next_state = build_cognitive_state(base_state=next_base_state, cognitive_stage=cognitive_stage)
    next_q_values = get_q_values_for_state(
        db=db,
        user_id=user_id,
        subtopic_id=subtopic_id,
        state=next_state,
    )
    next_max_q = max(next_q_values.values(), default=0.0)

    # Reward menjadi target update q-value. Reward naik jika jawaban benar,
    # mastery meningkat, dan akurasi assessment melewati batas.
    reward = q_agent.calculate_reward(
        is_correct=is_correct,
        mastery_before=mastery_before,
        mastery_after=progress.mastery,
        first_attempt=failures_before == 0,
        attempt_accuracy=attempt_accuracy,
    )
    actions = normalize_action_sequence(
        action_sequence=action_sequence,
        selected_action=selected_action,
        assessment_type=assessment_type,
    )
    updated_q_values: dict[str, float] = {}
    for action, credit in build_action_credits(actions).items():
        q_value = get_or_create_q_value(
            db=db,
            user_id=user_id,
            subtopic_id=subtopic_id,
            state=state,
            action=action,
        )
        credited_reward = reward * credit
        q_value.value = q_agent.update_q_value(
            current_q=q_value.value,
            reward=credited_reward,
            next_max_q=next_max_q,
        )
        updated_q_values[action] = q_value.value

        # InteractionLog menjadi bukti historis untuk debug, rapor, dan analisis model.
        db.add(InteractionLog(
            user_id=user_id,
            subtopic_id=subtopic_id,
            state=state,
            action=action,
            reward=credited_reward,
            score=1.0 if is_correct else 0.0,
            duration_seconds=duration_seconds,
        ))

    return {
        "reward": reward,
        "new_mastery": progress.mastery,
        "state": state,
        "next_state": next_state,
        "action": selected_action,
        "q_value": updated_q_values.get(selected_action, next(iter(updated_q_values.values()), 0.0)),
        "updated_q_values": updated_q_values,
        "cognitive_stage": cognitive_stage,
    }


# Bagian menghitung mastery modul untuk GKT dari mastery subtopik.
def build_topic_mastery(db: Session, user_id: int) -> dict[str, float]:
    # GKT bekerja pada level modul, maka mastery modul dihitung dari rata-rata mastery subtopik.
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


# Bagian membuat initial state neural GKT dari pre test atau mastery modul.
def build_topic_initial_state(db: Session, user_id: int) -> dict[str, float]:
    # Neural GKT memakai pre test sebagai initial state jika tersedia.
    # Kalau belum ada pre test, sistem memakai mastery modul saat ini sebagai fallback.
    modules = db.query(Module).all()
    initial_state: dict[str, float] = {}
    topic_mastery = build_topic_mastery(db=db, user_id=user_id)

    for module in modules:
        latest_pretest = db.query(AssessmentAttempt).filter(
            AssessmentAttempt.user_id == user_id,
            AssessmentAttempt.module_id == module.id,
            AssessmentAttempt.assessment_type == "pre_test",
            AssessmentAttempt.finished_at.isnot(None),
        ).order_by(AssessmentAttempt.finished_at.desc()).first()

        if latest_pretest:
            initial_state[module.id] = (latest_pretest.percentage or 0.0) / 100.0
        else:
            initial_state[module.id] = topic_mastery.get(module.id, 0.0) / 100.0

    return initial_state


# Bagian membangun graph prasyarat antar modul/topik.
def build_prerequisite_graph(db: Session) -> dict[str, list[dict]]:
    # Graph prasyarat menentukan hubungan antar modul/topik pada layer GKT.
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


# Bagian rekomendasi learning path: neural GKT untuk modul, q-learning untuk subtopik.
def recommend_next_step(db: Session, user_id: int, current_module_id: str, current_subtopic_id: str) -> dict:
    # Fungsi ini menggabungkan dua layer learning path:
    # macro layer: neural GKT / graph fallback memilih modul yang layak dipelajari
    # micro layer: q-learning memilih action belajar pada subtopik
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
    neural_gkt = load_neural_gkt_model()
    if neural_gkt and neural_gkt.is_trained:
        # Jika model neural sudah tersedia, prediksi mastery modul memakai message passing GKT.
        macro = neural_gkt.evaluate_mastery(
            current_topic_id=current_module_id,
            initial_state=build_topic_initial_state(db=db, user_id=user_id),
            prerequisites=prerequisite_graph,
        )
    else:
        # Jika belum ada model training, sistem tetap berjalan memakai graph prasyarat deterministik.
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
    cognitive_stage = get_cognitive_stage(db=db, user_id=user_id)
    base_state = q_agent.build_state(mastery=mastery, recent_failures=failures)
    state = build_cognitive_state(base_state=base_state, cognitive_stage=cognitive_stage)
    q_values = get_q_values_for_state(
        db=db,
        user_id=user_id,
        subtopic_id=recommended_subtopic_id,
        state=state,
    )
    q_value_states = get_q_values_for_subtopic(
        db=db,
        user_id=user_id,
        subtopic_id=recommended_subtopic_id,
    )
    allowed_actions = get_allowed_actions_for_stage(cognitive_stage)
    if has_learned_action_values(q_values=q_values, allowed_actions=allowed_actions):
        # Setelah q-value terbentuk, action dipilih dari nilai tertinggi pada state saat ini.
        action = q_agent.select_action(q_values, allowed_actions=allowed_actions)
    else:
        # Pada awal penggunaan, gunakan aturan cold start sampai data interaksi cukup.
        action = select_cold_start_action(
            mastery=mastery,
            failures=failures,
            cognitive_stage=cognitive_stage,
            can_review_previous=can_review_previous_subtopic(
                db=db,
                subtopic_id=recommended_subtopic_id,
            ),
        )
    cognitive_strategy = get_strategy_for_stage(cognitive_stage)

    reason = macro["reason"]
    if cognitive_stage != "unknown":
        reason = f"{reason} Profil kognitif dominan: {cognitive_stage}. {cognitive_strategy}"

    return {
        "macro_action": macro["action"],
        "recommended_module_id": recommended_module_id,
        "recommended_subtopic_id": recommended_subtopic_id,
        "micro_action": action,
        "state": state,
        "q_values": q_values,
        "q_value_states": q_value_states,
        "reason": reason,
        "macro_model": "neural_gkt" if neural_gkt and neural_gkt.is_trained else "graph_fallback",
        "neural_gkt_state": macro.get("neural_state", {}),
        "cognitive_stage": cognitive_stage,
        "cognitive_strategy": cognitive_strategy,
    }
