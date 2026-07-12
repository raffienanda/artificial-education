from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_optional_current_user
from app.models.user import User
from app.schemas.api_schemas import ChatbotMessageRequest, ChatbotMessageResponse

router = APIRouter()


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _message_id(prefix: str = "msg-ai") -> str:
    return f"{prefix}-{int(datetime.now(timezone.utc).timestamp() * 1000)}"


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
    _ = db, current_user
    return ChatbotMessageResponse(
        id=_message_id(),
        role="ai",
        content=_build_reply(payload.message),
        timestamp=_now_iso(),
    )
