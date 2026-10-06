import json
from pathlib import Path

from sqlalchemy.orm import Session

from app.data.seed_official_course import OFFICIAL_COURSE_ID
from app.models.module import Course
from app.models.question import Question


QUESTIONS_PATH = Path(__file__).with_name("official_questions.json")


def _assessment_questions(quiz_questions: list[dict]) -> list[dict]:
    """Reuse lecturer-authored items for module pre/post tests without inventing content."""
    grouped: dict[tuple[int, int], list[dict]] = {}
    for item in quiz_questions:
        _, module_number, subtopic_number, _ = item["id"].split("-")
        grouped.setdefault((int(module_number), int(subtopic_number)), []).append(item)

    assessments = []
    for module_number in range(1, 4):
        for subtopic_number in range(1, 6):
            items = grouped[(module_number, subtopic_number)]
            for assessment_type, source in (("pre_test", items[0]), ("post_test", items[-1])):
                assessments.append({
                    **source,
                    "id": f"voc-{assessment_type}-{module_number}-{subtopic_number}",
                    "assessment_type": assessment_type,
                })
    return assessments


def seed_official_questions(db: Session) -> int:
    """Add lecturer-authored assessments once without changing existing admin edits."""
    if not db.get(Course, OFFICIAL_COURSE_ID):
        return 0

    quiz_questions = json.loads(QUESTIONS_PATH.read_text(encoding="utf-8"))
    questions = quiz_questions + _assessment_questions(quiz_questions)
    existing_ids = {
        row.id for row in db.query(Question.id).filter(
            Question.id.in_([item["id"] for item in questions])
        ).all()
    }
    for item in questions:
        if item["id"] in existing_ids:
            continue
        db.add(Question(
            id=item["id"],
            subtopic_id=item["subtopic_id"],
            question_text=item["question_text"],
            options=item["options"],
            correct_answer=item["correct_answer"],
            explanation="",
            assessment_type=item["assessment_type"],
        ))

    inserted = len(questions) - len(existing_ids)
    if inserted:
        db.commit()
    return inserted
