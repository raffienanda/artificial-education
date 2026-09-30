import json
from pathlib import Path

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.module import Course, Module, Subtopic


OFFICIAL_COURSE_ID = "course-vocational-official"
LESSONS_PATH = Path(__file__).with_name("official_lessons.json")

MATERIALS = (
    (
        "materi-1",
        "Pendidikan Kejuruan dalam Konteks Global",
        "Transformasi dunia kerja, kesenjangan keterampilan, daya saing, dan posisi Indonesia dalam TVET global.",
        "kerangka-konteks-global.png",
        "Gambar 1. Kerangka konseptual pendidikan kejuruan dalam konteks global",
    ),
    (
        "materi-2",
        "Pendidikan sebagai Investasi Human Capital",
        "Teori human capital, hasil investasi pendidikan, kebutuhan industri, dan perencanaan pendidikan.",
        "kerangka-human-capital.png",
        "Gambar 2. Kerangka konseptual pendidikan sebagai investasi human capital",
    ),
    (
        "materi-3",
        "Landasan Filosofis dan Teoretis Pendidikan Vokasional",
        "Filsafat kerja, pendidikan berbasis kompetensi, pengalaman belajar, dan identitas profesional.",
        "kerangka-landasan-vokasional.png",
        "Gambar 3. Kerangka konseptual landasan filosofis dan teoretis pendidikan vokasional",
    ),
)


def seed_official_course(db: Session) -> bool:
    """Insert the initial lecturer material once; later admin edits remain authoritative."""
    if db.get(Course, OFFICIAL_COURSE_ID):
        return False

    lessons = json.loads(LESSONS_PATH.read_text(encoding="utf-8"))
    db.add(Course(
        id=OFFICIAL_COURSE_ID,
        title="Pendidikan Kejuruan",
        description="Materi resmi dari dosen: konteks global, investasi human capital, serta landasan pendidikan vokasional.",
        icon="book-open",
    ))

    for module_index, (key, title, description, image, caption) in enumerate(MATERIALS, start=1):
        module_id = f"module-vocational-{module_index}"
        db.add(Module(
            id=module_id,
            course_id=OFFICIAL_COURSE_ID,
            title=title,
            icon="book-open",
            description=description,
            difficulty="Dasar",
            estimated_time="Mandiri",
            order=module_index,
            status="in_progress",
        ))

        for part_index, part in enumerate(lessons[key]["sections"], start=1):
            figure = None
            if part_index == 1:
                figure = {
                    "src": f"/materi-dosen/figures/{image}",
                    "caption": caption,
                }
            db.add(Subtopic(
                id=f"{key}-{part_index}",
                module_id=module_id,
                title=part["title"],
                content={
                    "title": part["title"],
                    "tabs": [{"id": "ringkasan", "label": "Baca Materi", "icon": ""}],
                    "sections": [{
                        "type": "article",
                        "lesson": {
                            "figure": figure,
                            "intro": lessons[key]["intro"] if part_index == 1 else [],
                            "sections": [part],
                        },
                    }],
                },
            ))

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        if db.get(Course, OFFICIAL_COURSE_ID):
            return False
        raise
    return True
