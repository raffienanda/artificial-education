import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import app.models  # noqa: F401
from app.api.endpoints.modules import _enrich_module_with_user_progress
from app.api.endpoints.admin import update_module, update_subtopic
from app.core.database import Base
from app.data.seed_official_course import OFFICIAL_COURSE_ID, seed_official_course
from app.data.seed_official_questions import seed_official_questions
from app.models.module import Course, Module, Subtopic
from app.models.question import Question
from app.schemas.api_schemas import AdminModuleUpdate, AdminSubtopicUpdate, ModuleResponse


class OfficialCourseSeedTests(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        self.db = Session(self.engine)

    def tearDown(self):
        self.db.close()
        self.engine.dispose()

    def test_seed_creates_editable_course_without_overwriting_later_changes(self):
        self.assertTrue(seed_official_course(self.db))
        self.assertEqual(self.db.query(Course).filter_by(id=OFFICIAL_COURSE_ID).count(), 1)
        self.assertEqual(self.db.query(Module).filter_by(course_id=OFFICIAL_COURSE_ID).count(), 3)
        self.assertEqual(self.db.query(Subtopic).count(), 15)

        first = self.db.get(Subtopic, "materi-1-1")
        self.assertEqual(first.content["sections"][0]["lesson"]["figure"]["caption"],
                         "Gambar 1. Kerangka konseptual pendidikan kejuruan dalam konteks global")
        first.title = "Judul dari admin"
        self.db.commit()

        self.assertFalse(seed_official_course(self.db))
        self.assertEqual(self.db.get(Subtopic, "materi-1-1").title, "Judul dari admin")
        self.assertEqual(self.db.query(Subtopic).count(), 15)

    def test_official_modules_use_full_assessment_mode(self):
        seed_official_course(self.db)
        module = self.db.get(Module, "module-vocational-3")
        payload = _enrich_module_with_user_progress(module, self.db, 1, {})
        response = ModuleResponse.model_validate(payload)
        self.assertEqual(response.status, "locked")
        self.assertTrue(response.assessment_enabled)
        self.assertEqual(response.assessment_mode, "full")
        self.assertEqual(len(response.subtopics), 5)

    def test_lecturer_questions_are_insert_only(self):
        seed_official_course(self.db)
        self.assertEqual(seed_official_questions(self.db), 104)
        self.assertEqual(self.db.query(Question).filter_by(assessment_type="quiz").count(), 74)
        self.assertEqual(self.db.query(Question).filter_by(assessment_type="pre_test").count(), 15)
        self.assertEqual(self.db.query(Question).filter_by(assessment_type="post_test").count(), 15)
        self.assertEqual(self.db.query(Question).filter_by(subtopic_id="materi-3-5", assessment_type="quiz").count(), 4)
        self.assertIsNone(self.db.get(Question, "voc-3-5-2"))

        first = self.db.get(Question, "voc-1-1-1")
        first.question_text = "Revisi dari admin"
        self.db.commit()
        self.assertEqual(seed_official_questions(self.db), 0)
        self.assertEqual(self.db.get(Question, "voc-1-1-1").question_text, "Revisi dari admin")

    def test_admin_edit_is_returned_to_student(self):
        seed_official_course(self.db)
        original = self.db.get(Subtopic, "materi-2-1")
        revised = dict(original.content)
        revised["title"] = "Judul revisi"
        update_subtopic(
            "materi-2-1",
            AdminSubtopicUpdate(title="Judul revisi", content=revised),
            db=self.db,
            _=None,
        )

        module = self.db.get(Module, "module-vocational-2")
        student_module = _enrich_module_with_user_progress(module, self.db, 1, {})
        self.assertEqual(student_module["subtopics"][0]["title"], "Judul revisi")
        self.assertEqual(student_module["subtopics"][0]["content"]["title"], "Judul revisi")

    def test_admin_can_update_module_title(self):
        seed_official_course(self.db)
        update_module(
            "module-vocational-1",
            AdminModuleUpdate(title="Judul modul baru", description="Deskripsi baru"),
            db=self.db,
            _=None,
        )
        module = self.db.get(Module, "module-vocational-1")
        student_module = _enrich_module_with_user_progress(module, self.db, 1, {})
        self.assertEqual(student_module["title"], "Judul modul baru")
        self.assertEqual(student_module["description"], "Deskripsi baru")


if __name__ == "__main__":
    unittest.main()
