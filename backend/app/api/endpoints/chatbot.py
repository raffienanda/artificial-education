import json
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.core.security import get_optional_current_user
from app.models.assessment import AssessmentAttempt
from app.models.cognitive import CognitiveProfile
from app.models.learning_path import QValue
from app.models.module import Module, Subtopic
from app.models.progress import UserProgress
from app.models.user import User
from app.schemas.api_schemas import ChatbotMessageRequest, ChatbotMessageResponse

router = APIRouter()


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _message_id(prefix: str = "msg-ai") -> str:
    return f"{prefix}-{int(datetime.now(timezone.utc).timestamp() * 1000)}"


def _flatten_content(value, limit: int = 900) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value[:limit]
    if isinstance(value, list):
        return " ".join(_flatten_content(item, limit) for item in value)[:limit]
    if isinstance(value, dict):
        parts = []
        for key, item in value.items():
            if key in {"icon", "id"}:
                continue
            parts.append(_flatten_content(item, limit))
        return " ".join(part for part in parts if part)[:limit]
    return str(value)[:limit]


def _build_learning_context(
    db: Session,
    current_user: User | None,
    module_id: str | None,
    subtopic_id: str | None,
) -> str:
    if not current_user:
        return "mahasiswa belum login, jadi konteks personal belum tersedia."

    module = db.query(Module).filter(Module.id == module_id).first() if module_id else None
    subtopic = db.query(Subtopic).filter(Subtopic.id == subtopic_id).first() if subtopic_id else None
    if not module and subtopic:
        module = db.query(Module).filter(Module.id == subtopic.module_id).first()

    progress_rows = db.query(UserProgress).filter(UserProgress.user_id == current_user.id).all()
    progress_map = {row.topic_id: row for row in progress_rows}
    current_progress = progress_map.get(subtopic.id) if subtopic else None
    module_subtopics = (
        db.query(Subtopic).filter(Subtopic.module_id == module.id).order_by(Subtopic.id).all()
        if module
        else []
    )

    q_values = (
        db.query(QValue)
        .filter(QValue.user_id == current_user.id)
        .filter(QValue.subtopic_id == subtopic.id)
        .order_by(QValue.value.desc())
        .limit(8)
        .all()
        if subtopic
        else []
    )
    cognitive = (
        db.query(CognitiveProfile)
        .filter(CognitiveProfile.user_id == current_user.id)
        .first()
    )
    attempts = (
        db.query(AssessmentAttempt)
        .filter(AssessmentAttempt.user_id == current_user.id)
        .order_by(AssessmentAttempt.finished_at.desc().nullslast(), AssessmentAttempt.started_at.desc())
        .limit(6)
        .all()
    )

    lines = [
        f"nama_mahasiswa: {current_user.display_name or current_user.username}",
        f"username: {current_user.username}",
        f"xp: {current_user.xp or 0}",
        f"reward_points: {current_user.reward_points or 0}",
    ]
    if module:
        lines.append(f"modul_aktif: {module.title} ({module.id})")
        lines.append(f"deskripsi_modul: {module.description}")
    if subtopic:
        lines.append(f"subtopik_aktif: {subtopic.title} ({subtopic.id})")
        lines.append(f"materi_subtopik: {_flatten_content(subtopic.content)}")
    if current_progress:
        lines.append(
            "progress_subtopik_aktif: "
            f"mastery={round(current_progress.mastery or 0, 2)}%, status={current_progress.status}"
        )
    if module_subtopics:
        subtopic_summary = []
        for item in module_subtopics:
            item_progress = progress_map.get(item.id)
            mastery = round(item_progress.mastery or 0, 2) if item_progress else 0
            status = item_progress.status if item_progress else "belum mulai"
            subtopic_summary.append(f"{item.title}: {mastery}%/{status}")
        lines.append(f"ringkasan_progress_modul: {'; '.join(subtopic_summary)}")
    if q_values:
        lines.append(
            "q_values_subtopik_aktif: "
            + "; ".join(f"{row.state} -> {row.action} = {round(row.value or 0, 4)}" for row in q_values)
        )
    else:
        lines.append("q_values_subtopik_aktif: belum ada interaksi q-learning")
    if cognitive:
        lines.append(
            "profil_kognitif: "
            f"dominant_stage={cognitive.dominant_stage}, "
            f"dualism={round(cognitive.dualism_score or 0, 2)}, "
            f"multiplicity={round(cognitive.multiplicity_score or 0, 2)}, "
            f"relativism={round(cognitive.relativism_score or 0, 2)}, "
            f"commitment={round(cognitive.commitment_score or 0, 2)}"
        )
    else:
        lines.append("profil_kognitif: belum diisi")
    if attempts:
        lines.append(
            "attempt_terakhir: "
            + "; ".join(
                f"{item.assessment_type} {item.module_id}/{item.subtopic_id or '-'} "
                f"{round(item.percentage or 0, 2)}% passed={item.passed}"
                for item in attempts
            )
        )
    return "\n".join(lines)


def _build_gemini_prompt(message: str, context: str) -> str:
    return f"""
kamu adalah chatbot tutor di aplikasi cogniVA, aplikasi learning path adaptif untuk mahasiswa.

aturan jawaban:
- jawab dalam bahasa indonesia yang santai, jelas, dan tidak kaku.
- fokus membantu mahasiswa belajar, bukan memberi label psikologis.
- kalau mahasiswa bertanya soal quiz, beri hint dan penjelasan konsep, jangan langsung memberi jawaban final kecuali diminta evaluasi umum.
- gunakan konteks progress, q-value, mastery, post test, dan profil kognitif kalau relevan.
- jangan mengarang data di luar konteks yang tersedia.
- jawaban maksimal 4 paragraf pendek.

konteks dari database:
{context}

pertanyaan mahasiswa:
{message}
""".strip()


def _extract_gemini_text(data: dict) -> str:
    candidates = data.get("candidates") or []
    if not candidates:
        return ""
    parts = candidates[0].get("content", {}).get("parts", [])
    return "\n".join(part.get("text", "") for part in parts if part.get("text")).strip()


def _ask_gemini(prompt: str) -> str | None:
    if not settings.GEMINI_API_KEY:
        return None

    endpoint = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"{settings.GEMINI_MODEL}:generateContent"
    )
    body = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": prompt}],
            }
        ],
        "generationConfig": {
            "temperature": 0.4,
            "maxOutputTokens": 450,
        },
    }
    request = Request(
        endpoint,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": settings.GEMINI_API_KEY,
        },
        method="POST",
    )

    try:
        with urlopen(request, timeout=20) as response:
            payload = json.loads(response.read().decode("utf-8"))
            return _extract_gemini_text(payload) or None
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError):
        return None


def _build_reply(message: str) -> str:
    text = message.lower().strip()

    if any(keyword in text for keyword in ("q value", "q-value", "qvalue", "bellman")):
        return (
            "q-value berubah setelah kamu mengerjakan soal yang tersambung ke subtopik. "
            "jawaban benar, akurasi percobaan, dan durasi belajar dihitung sebagai reward, lalu sistem memperbarui nilai aksi belajar dengan persamaan bellman."
        )

    if any(keyword in text for keyword in ("pre test", "pretest")):
        return (
            "pre test dipakai untuk membaca kemampuan awal pada satu modul sebelum materi dibuka. "
            "hasilnya membantu sistem membentuk state awal pembelajaran."
        )

    if any(keyword in text for keyword in ("post test", "posttest", "rapor")):
        return (
            "post test muncul setelah semua quiz subtopik pada modul selesai. "
            "hasil akhirnya dipakai untuk rapor modul dan keputusan apakah modul berikutnya bisa dibuka."
        )

    if any(keyword in text for keyword in ("terkunci", "lock", "modul")):
        return (
            "modul dan subtopik dibuka bertahap. selesaikan pre test modul, lalu quiz subtopik sesuai urutan. "
            "modul berikutnya baru terbuka kalau syarat modul sebelumnya terpenuhi."
        )

    if any(keyword in text for keyword in ("salah", "bingung", "belum paham", "ulang")):
        return (
            "kalau masih bingung, coba ulangi ringkasan materi dulu lalu kerjakan drill soal. "
            "drill membantu latihan tanpa langsung menjadi evaluasi akhir modul."
        )

    return (
        "aku bisa bantu jelaskan alur belajar, pre test, quiz, post test, q-value, atau kenapa modul masih terkunci. "
        "tulis bagian yang ingin kamu pahami, nanti aku arahkan sesuai progres belajarmu."
    )


@router.get("/conversation", response_model=list[ChatbotMessageResponse])
def get_conversation(
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_optional_current_user),
):
    _ = db, current_user
    return [
        ChatbotMessageResponse(
            id="msg-ai-welcome",
            role="ai",
            content="halo, aku tutor belajar kamu. kalau ada materi, quiz, q-value, atau modul yang terkunci, tanya saja di sini.",
            timestamp=_now_iso(),
        )
    ]


@router.post("/message", response_model=ChatbotMessageResponse)
def send_message(
    payload: ChatbotMessageRequest,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_optional_current_user),
):
    context = _build_learning_context(
        db=db,
        current_user=current_user,
        module_id=payload.module_id,
        subtopic_id=payload.subtopic_id,
    )
    gemini_reply = _ask_gemini(_build_gemini_prompt(payload.message, context))

    return ChatbotMessageResponse(
        id=_message_id(),
        role="ai",
        content=gemini_reply or _build_reply(payload.message),
        timestamp=_now_iso(),
    )
