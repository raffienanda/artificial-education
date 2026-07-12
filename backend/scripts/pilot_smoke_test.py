from __future__ import annotations

import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core.database import SessionLocal
from app.models.cognitive import CognitiveItem
from app.models.question import Question


BASE_URL = "http://127.0.0.1:8000"
MODULE_IDS = ("mod-001", "mod-002", "mod-003")


@dataclass
class ApiSession:
    token: str = ""

    def request(self, method: str, path: str, payload: dict | None = None) -> tuple[int, dict | list]:
        data = json.dumps(payload).encode("utf-8") if payload is not None else None
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        request = urllib.request.Request(
            f"{BASE_URL}{path}",
            data=data,
            headers=headers,
            method=method,
        )
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                body = response.read().decode("utf-8")
                return response.status, json.loads(body) if body else {}
        except urllib.error.HTTPError as error:
            body = error.read().decode("utf-8")
            try:
                parsed = json.loads(body)
            except json.JSONDecodeError:
                parsed = {"detail": body}
            return error.code, parsed


def get_correct_questions(module_id: str, assessment_type: str, subtopic_id: str | None = None) -> list[Question]:
    db = SessionLocal()
    query = db.query(Question).filter(Question.assessment_type == assessment_type)
    if subtopic_id:
        query = query.filter(Question.subtopic_id == subtopic_id)
    else:
        query = query.filter(Question.subtopic_id.like(f"sub-{module_id.split('-')[1]}-%"))
    questions = query.order_by(Question.id).all()
    for question in questions:
        db.expunge(question)
    db.close()
    return questions


def submit_questions(session: ApiSession, questions: list[Question], action: str) -> list[dict]:
    feedback: list[dict] = []
    for question in questions:
        status, result = session.request(
            "POST",
            "/api/quiz/submit",
            {
                "question_id": question.id,
                "selected_option_id": question.correct_answer,
                "action": action,
                "duration_seconds": 8,
            },
        )
        assert status == 200, f"submit failed {question.id}: {status} {result}"
        feedback.append(result)
    return feedback


def main() -> None:
    session = ApiSession()
    username = f"pilot_{int(time.time())}"
    password = "password123"

    status, auth = session.request(
        "POST",
        "/api/auth/register",
        {"username": username, "password": password, "display_name": "Pilot Test Student"},
    )
    assert status == 200, f"register failed: {status} {auth}"
    session.token = auth["access_token"]

    status, modules = session.request("GET", "/api/modules/")
    assert status == 200 and len(modules) == 3, f"module fetch failed: {status} {modules}"
    assert modules[0]["status"] == "in_progress", f"module 1 should unlock first: {modules[0]['status']}"

    status, items = session.request("GET", "/api/cognitive/items")
    assert status == 200 and len(items) >= 16, "cognitive items missing"
    responses = [{"item_id": item["id"], "score": 4 if index % 3 else 3} for index, item in enumerate(items)]
    status, profile = session.request("POST", "/api/cognitive/responses", {"responses": responses})
    assert status == 200 and profile.get("dominant_stage"), f"cognitive submit failed: {status} {profile}"

    summary: dict[str, dict] = {
        "user": {"username": username},
        "modules": {},
    }

    action_by_subtopic_index = {
        0: "show_text",
        1: "show_video",
        2: "easy_quiz",
        3: "show_video",
        4: "show_text",
    }

    for module_id in MODULE_IDS:
        pretest_feedback = submit_questions(session, get_correct_questions(module_id, "pre_test"), "pre_test")
        status, modules_after_pretest = session.request("GET", "/api/modules/")
        assert status == 200, f"module refresh failed after pretest {module_id}"

        module = next(item for item in modules_after_pretest if item["id"] == module_id)
        quiz_count = 0
        for index, subtopic in enumerate(module["subtopics"]):
            quiz_feedback = submit_questions(
                session,
                get_correct_questions(module_id, "quiz", subtopic["id"]),
                action_by_subtopic_index.get(index, "show_text"),
            )
            quiz_count += len(quiz_feedback)

        posttest_feedback = submit_questions(session, get_correct_questions(module_id, "post_test"), "post_test")
        status, refreshed_modules = session.request("GET", "/api/modules/")
        assert status == 200, f"module refresh failed after posttest {module_id}"
        refreshed_module = next(item for item in refreshed_modules if item["id"] == module_id)

        summary["modules"][module_id] = {
            "pre_test_items": len(pretest_feedback),
            "quiz_items": quiz_count,
            "post_test_items": len(posttest_feedback),
            "status_after": refreshed_module["status"],
        }

    status, logs = session.request("GET", "/api/recommendation/logs?limit=50")
    assert status == 200 and len(logs) > 0, "interaction logs missing"
    summary["interaction_logs_checked"] = len(logs)

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
