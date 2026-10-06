import unittest

from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import app.models  # noqa: F401
from app.api.endpoints.modules import _enrich_module_with_user_progress
from app.api.endpoints.progress import get_learning_gates, get_module_diagnosis
from app.api.endpoints.quiz import get_questions, submit_answer
from app.core.database import Base
from app.data.seed_official_course import seed_official_course
from app.data.seed_official_questions import seed_official_questions
from app.models.learning_path import TopicPrerequisite
from app.models.module import Course, Module
from app.models.question import Question
from app.models.user import User
from app.schemas.api_schemas import AnswerSubmission
from app.services.learning_path import build_prerequisite_graph, recommend_next_step


class OfficialQuizTests(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        self.db = Session(self.engine)
        seed_official_course(self.db)
        seed_official_questions(self.db)
        self.user = User(username="student", display_name="Student", password_hash="unused")
        self.db.add(self.user)
        self.db.commit()

    def tearDown(self):
        self.db.close()
        self.engine.dispose()

    def complete_assessment(self, module_id, assessment_type, subtopic_id=None):
        questions = get_questions(
            module_id,
            assessment_type=assessment_type,
            subtopic_id=subtopic_id,
            db=self.db,
            current_user=self.user,
        )
        for question in questions:
            answer = self.db.get(Question, question.id)
            submit_answer(
                AnswerSubmission(
                    question_id=question.id,
                    selected_option_id=answer.correct_answer,
                    action=assessment_type,
                    action_sequence=[assessment_type],
                ),
                db=self.db,
                current_user=self.user,
            )
        return questions

    def test_full_demo_flow_awards_points_and_unlocks_posttest(self):
        with self.assertRaises(HTTPException):
            get_questions(
                "module-vocational-1",
                assessment_type="quiz",
                subtopic_id="materi-1-1",
                db=self.db,
                current_user=self.user,
            )

        pretest = self.complete_assessment("module-vocational-1", "pre_test")
        self.assertEqual(len(pretest), 5)
        questions = get_questions(
            "module-vocational-1",
            assessment_type="quiz",
            subtopic_id="materi-1-1",
            db=self.db,
            current_user=self.user,
        )
        self.assertEqual(len(questions), 5)

        for question in questions:
            answer = self.db.get(Question, question.id)
            feedback = submit_answer(
                AnswerSubmission(
                    question_id=question.id,
                    selected_option_id=answer.correct_answer,
                    action="easy_quiz",
                    action_sequence=["easy_quiz"],
                ),
                db=self.db,
                current_user=self.user,
            )
            self.assertTrue(feedback.correct)

        self.db.refresh(self.user)
        self.assertGreater(self.user.xp, 0)
        self.assertGreater(self.user.reward_points, 0)
        module = self.db.get(Module, "module-vocational-1")
        payload = _enrich_module_with_user_progress(module, self.db, self.user.id, {})
        self.assertTrue(payload["subtopics"][0]["completed"])

        with self.assertRaises(HTTPException):
            get_questions("module-vocational-1", assessment_type="post_test", db=self.db, current_user=self.user)

        for index in range(2, 6):
            self.complete_assessment("module-vocational-1", "quiz", f"materi-1-{index}")
        posttest = get_questions("module-vocational-1", assessment_type="post_test", db=self.db, current_user=self.user)
        self.assertEqual(len(posttest), 5)

    def test_unfinished_quiz_does_not_complete_subtopic(self):
        self.complete_assessment("module-vocational-1", "pre_test")
        questions = get_questions(
            "module-vocational-1",
            assessment_type="quiz",
            subtopic_id="materi-1-1",
            db=self.db,
            current_user=self.user,
        )
        for question in questions[:3]:
            answer = self.db.get(Question, question.id)
            submit_answer(
                AnswerSubmission(
                    question_id=question.id,
                    selected_option_id=answer.correct_answer,
                    action="easy_quiz",
                    action_sequence=["easy_quiz"],
                ),
                db=self.db,
                current_user=self.user,
            )

        gates = get_learning_gates(db=self.db, current_user=self.user)
        self.assertNotIn("module-vocational-1:materi-1-1", gates["completed_subtopic_quizzes"])
        self.assertFalse(gates["passed_modules"]["module-vocational-1"])

    def test_one_correct_answer_does_not_unlock_next_subtopic(self):
        self.complete_assessment("module-vocational-1", "pre_test")
        questions = get_questions(
            "module-vocational-1",
            assessment_type="quiz",
            subtopic_id="materi-1-1",
            db=self.db,
            current_user=self.user,
        )

        final_feedback = None
        for index, question in enumerate(questions):
            answer = self.db.get(Question, question.id)
            selected_option = answer.correct_answer
            if index > 0:
                selected_option = next(
                    option["id"] for option in answer.options if option["id"] != answer.correct_answer
                )
            final_feedback = submit_answer(
                AnswerSubmission(
                    question_id=question.id,
                    selected_option_id=selected_option,
                    action="easy_quiz",
                    action_sequence=["easy_quiz"],
                ),
                db=self.db,
                current_user=self.user,
            )

        self.assertIsNotNone(final_feedback)
        self.assertTrue(final_feedback.attempt_finished)
        self.assertFalse(final_feedback.attempt_passed)
        self.assertEqual(final_feedback.attempt_score, 1)
        self.assertEqual(final_feedback.attempt_percentage, 20.0)

        gates = get_learning_gates(db=self.db, current_user=self.user)
        self.assertNotIn("module-vocational-1:materi-1-1", gates["completed_subtopic_quizzes"])
        with self.assertRaises(HTTPException):
            get_questions(
                "module-vocational-1",
                assessment_type="quiz",
                subtopic_id="materi-1-2",
                db=self.db,
                current_user=self.user,
            )

    def test_recommendation_uses_official_course_graph_and_available_actions(self):
        self.db.add(Course(id="demo", title="Demo"))
        self.db.add_all([
            Module(id="mod-001", course_id="demo", title="Demo 1", order=1),
            Module(id="mod-002", course_id="demo", title="Demo 2", order=2),
        ])
        self.db.flush()
        self.db.add(TopicPrerequisite(topic_id="mod-002", prerequisite_id="mod-001"))
        self.db.commit()

        graph = build_prerequisite_graph(self.db, course_id="course-vocational-official")
        self.assertEqual(graph["module-vocational-2"][0]["id"], "module-vocational-1")
        self.assertNotIn("mod-002", graph)
        recommendation = recommend_next_step(
            self.db, self.user.id, "module-vocational-2", "materi-2-1"
        )
        self.assertEqual(recommendation["macro_model"], "graph_fallback")
        self.assertEqual(recommendation["macro_action"], "back_trace")
        self.assertEqual(recommendation["recommended_module_id"], "module-vocational-1")
        self.assertIn(recommendation["micro_action"], {"show_text", "easy_quiz", "review_previous"})

    def test_module_report_uses_complete_demo_assessment_flow(self):
        before = get_module_diagnosis("module-vocational-1", db=self.db, current_user=self.user)
        self.assertFalse(before["available"])

        self.complete_assessment("module-vocational-1", "pre_test")
        for index in range(1, 6):
            self.complete_assessment("module-vocational-1", "quiz", f"materi-1-{index}")
        self.complete_assessment("module-vocational-1", "post_test")

        report = get_module_diagnosis("module-vocational-1", db=self.db, current_user=self.user)
        self.assertTrue(report["available"])
        self.assertEqual(report["assessment_mode"], "full")
        self.assertEqual(report["quiz_average"], 100)
        self.assertEqual(report["pre_test_score"], 100)
        self.assertEqual(report["post_test_score"], 100)
        self.assertTrue(report["can_continue"])
        self.assertFalse(report["can_retake_post_test"])


if __name__ == "__main__":
    unittest.main()
