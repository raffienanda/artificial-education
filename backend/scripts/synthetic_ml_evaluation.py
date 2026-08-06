from __future__ import annotations

import csv
import json
import math
import random
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = ROOT / "docs" / "evaluation"
RANDOM_SEED = 20260709

MODULES = {
    "mod-001": ["sub-001-1", "sub-001-2", "sub-001-3", "sub-001-4", "sub-001-5"],
    "mod-002": ["sub-002-1", "sub-002-2", "sub-002-3", "sub-002-4", "sub-002-5"],
    "mod-003": ["sub-003-1", "sub-003-2", "sub-003-3", "sub-003-4", "sub-003-5"],
}

EDGES = {
    "mod-002": ["mod-001"],
    "mod-003": ["mod-002"],
}

ACTIONS = ("show_text", "show_video", "easy_quiz", "hard_quiz", "review_previous")
COGNITIVE_STAGES = ("dualism", "multiplicity", "relativism", "commitment")


@dataclass(frozen=True)
class Student:
    student_id: str
    ability: float
    cognitive_stage: str
    preferred_action: str


def sigmoid(value: float) -> float:
    return 1.0 / (1.0 + math.exp(-value))


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def mastery_bucket(mastery: float) -> str:
    if mastery >= 0.8:
        return "high"
    if mastery >= 0.5:
        return "medium"
    return "low"


def build_students(rng: random.Random, total: int = 120) -> list[Student]:
    stage_to_preference = {
        "dualism": "show_text",
        "multiplicity": "show_video",
        "relativism": "easy_quiz",
        "commitment": "hard_quiz",
    }
    students: list[Student] = []
    for index in range(total):
        stage = rng.choices(COGNITIVE_STAGES, weights=(0.28, 0.34, 0.25, 0.13), k=1)[0]
        ability = clamp(rng.gauss(0.56, 0.18))
        students.append(
            Student(
                student_id=f"synthetic-{index + 1:03d}",
                ability=ability,
                cognitive_stage=stage,
                preferred_action=stage_to_preference[stage],
            )
        )
    return students


def simulate_pretest_and_true_mastery(
    rng: random.Random,
    students: list[Student],
) -> tuple[list[dict], dict[tuple[str, str], float], dict[tuple[str, str], float]]:
    rows: list[dict] = []
    pretest_state: dict[tuple[str, str], float] = {}
    true_mastery: dict[tuple[str, str], float] = {}

    for student in students:
        previous_module_mastery = student.ability
        for module_index, (module_id, subtopics) in enumerate(MODULES.items(), start=1):
            prerequisite_bonus = 0.16 * (previous_module_mastery - 0.5)
            module_difficulty = 0.08 * (module_index - 1)
            module_mastery = clamp(student.ability + prerequisite_bonus - module_difficulty + rng.gauss(0, 0.08))
            pretest_correct = 0

            for subtopic_id in subtopics:
                subtopic_variation = rng.gauss(0, 0.07)
                mastery = clamp(module_mastery + subtopic_variation)
                true_mastery[(student.student_id, subtopic_id)] = mastery
                correct = rng.random() < mastery
                pretest_correct += int(correct)
                rows.append(
                    {
                        "student_id": student.student_id,
                        "module_id": module_id,
                        "subtopic_id": subtopic_id,
                        "event_type": "pre_test",
                        "action": "pre_test",
                        "correct": int(correct),
                        "true_mastery": round(mastery, 4),
                        "cognitive_stage": student.cognitive_stage,
                    }
                )

            pretest_state[(student.student_id, module_id)] = pretest_correct / len(subtopics)
            previous_module_mastery = module_mastery

    return rows, pretest_state, true_mastery


def predict_without_graph(student: Student, module_id: str, pretest_state: dict[tuple[str, str], float]) -> float:
    return pretest_state[(student.student_id, module_id)]


def predict_with_graph(student: Student, module_id: str, pretest_state: dict[tuple[str, str], float]) -> float:
    own = pretest_state[(student.student_id, module_id)]
    prerequisites = EDGES.get(module_id, [])
    if not prerequisites:
        return own
    prerequisite_signal = sum(pretest_state[(student.student_id, item)] for item in prerequisites) / len(prerequisites)
    return clamp((0.72 * own) + (0.28 * prerequisite_signal))


def binary_metrics(y_true: list[int], y_score: list[float], threshold: float = 0.6) -> dict[str, float]:
    y_pred = [1 if score >= threshold else 0 for score in y_score]
    tp = sum(1 for true, pred in zip(y_true, y_pred) if true == 1 and pred == 1)
    tn = sum(1 for true, pred in zip(y_true, y_pred) if true == 0 and pred == 0)
    fp = sum(1 for true, pred in zip(y_true, y_pred) if true == 0 and pred == 1)
    fn = sum(1 for true, pred in zip(y_true, y_pred) if true == 1 and pred == 0)
    total = max(1, len(y_true))
    accuracy = (tp + tn) / total
    precision = tp / max(1, tp + fp)
    recall = tp / max(1, tp + fn)
    f1 = 2 * precision * recall / max(1e-9, precision + recall)
    mae = sum(abs(true - score) for true, score in zip(y_true, y_score)) / total
    rmse = math.sqrt(sum((true - score) ** 2 for true, score in zip(y_true, y_score)) / total)
    return {
        "accuracy": round(accuracy, 4),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
        "mae": round(mae, 4),
        "rmse": round(rmse, 4),
    }


def evaluate_neural_gkt_bootstrap(
    rng: random.Random,
    students: list[Student],
    rows: list[dict],
    pretest_state: dict[tuple[str, str], float],
) -> tuple[dict, list[dict]]:
    y_true: list[int] = []
    baseline_scores: list[float] = []
    graph_scores: list[float] = []
    test_rows: list[dict] = []

    for student in students:
        for module_id, subtopics in MODULES.items():
            for subtopic_id in subtopics:
                baseline = predict_without_graph(student, module_id, pretest_state)
                graph = predict_with_graph(student, module_id, pretest_state)
                # Synthetic post-test correctness depends on true graph-aware knowledge plus noise.
                probability = clamp((0.66 * graph) + (0.34 * student.ability) + rng.gauss(0, 0.05))
                correct = int(rng.random() < probability)
                y_true.append(correct)
                baseline_scores.append(baseline)
                graph_scores.append(graph)
                test_rows.append(
                    {
                        "student_id": student.student_id,
                        "module_id": module_id,
                        "subtopic_id": subtopic_id,
                        "event_type": "post_test",
                        "action": "post_test",
                        "correct": correct,
                        "gkt_baseline_score": round(baseline, 4),
                        "gkt_graph_score": round(graph, 4),
                        "cognitive_stage": student.cognitive_stage,
                    }
                )

    rows.extend(test_rows)
    return {
        "baseline_no_graph": binary_metrics(y_true, baseline_scores),
        "neural_gkt_bootstrap": binary_metrics(y_true, graph_scores),
        "test_samples": len(y_true),
    }, rows


def reward_for_action(action: str, student: Student, mastery: float, difficulty: float, rng: random.Random) -> tuple[float, float, int]:
    action_bonus = {
        "show_text": 0.10 if student.cognitive_stage == "dualism" else 0.03,
        "show_video": 0.10 if student.cognitive_stage == "multiplicity" else 0.04,
        "easy_quiz": 0.10 if mastery < 0.65 else 0.03,
        "hard_quiz": 0.12 if mastery >= 0.65 else -0.04,
        "review_previous": 0.11 if mastery < 0.45 else 0.01,
    }[action]
    probability = clamp(student.ability + mastery * 0.45 + action_bonus - difficulty + rng.gauss(0, 0.06))
    correct = int(rng.random() < probability)
    mastery_gain = (0.06 if correct else -0.035) + action_bonus * 0.35
    reward = (100 if correct else -10) + (mastery_gain * 100)
    return reward, mastery_gain, correct


def choose_q_action(q_table: dict[tuple[str, str], float], state: str, epsilon: float, rng: random.Random) -> str:
    if rng.random() < epsilon:
        return rng.choice(ACTIONS)
    return max(ACTIONS, key=lambda action: (q_table[(state, action)], -ACTIONS.index(action)))


def simulate_q_learning(students: list[Student], episodes: int = 18) -> dict:
    adaptive_rng = random.Random(RANDOM_SEED + 100)
    random_rng = random.Random(RANDOM_SEED + 200)
    q_table: dict[tuple[str, str], float] = defaultdict(float)
    alpha = 0.1
    gamma = 0.9
    adaptive_rows: list[dict] = []
    random_rows: list[dict] = []

    def run_policy(policy_name: str, rng: random.Random, use_q: bool) -> tuple[list[float], list[dict]]:
        post_scores: list[float] = []
        output_rows: list[dict] = []
        for student in students:
            mastery = clamp(student.ability * 0.55 + rng.gauss(0, 0.07))
            for episode in range(episodes):
                state = f"{mastery_bucket(mastery)}:{student.cognitive_stage}"
                difficulty = 0.05 + 0.015 * episode
                if use_q:
                    epsilon = max(0.05, 0.35 - (episode * 0.015))
                    action = choose_q_action(q_table, state, epsilon, rng)
                else:
                    action = rng.choice(ACTIONS)
                reward, mastery_gain, correct = reward_for_action(action, student, mastery, difficulty, rng)
                new_mastery = clamp(mastery + mastery_gain)
                next_state = f"{mastery_bucket(new_mastery)}:{student.cognitive_stage}"

                if use_q:
                    current_q = q_table[(state, action)]
                    next_max_q = max(q_table[(next_state, next_action)] for next_action in ACTIONS)
                    q_table[(state, action)] = current_q + alpha * (reward + gamma * next_max_q - current_q)

                output_rows.append(
                    {
                        "student_id": student.student_id,
                        "episode": episode + 1,
                        "policy": policy_name,
                        "state": state,
                        "action": action,
                        "correct": correct,
                        "reward": round(reward, 4),
                        "mastery_before": round(mastery, 4),
                        "mastery_after": round(new_mastery, 4),
                    }
                )
                mastery = new_mastery
            post_scores.append(mastery)
        return post_scores, output_rows

    adaptive_scores, adaptive_rows = run_policy("q_learning_adaptive", adaptive_rng, use_q=True)
    random_scores, random_rows = run_policy("random_policy", random_rng, use_q=False)
    q_values = [
        {"state": state, "action": action, "q_value": round(value, 4)}
        for (state, action), value in sorted(q_table.items())
        if abs(value) > 0.0001
    ]

    def summary(scores: list[float]) -> dict[str, float]:
        passed = sum(1 for score in scores if score >= 0.6)
        return {
            "mean_final_mastery": round(sum(scores) / len(scores), 4),
            "pass_rate_60": round(passed / len(scores), 4),
        }

    adaptive_summary = summary(adaptive_scores)
    random_summary = summary(random_scores)
    return {
        "adaptive": adaptive_summary,
        "random_baseline": random_summary,
        "relative_mastery_gain": round(
            adaptive_summary["mean_final_mastery"] - random_summary["mean_final_mastery"], 4
        ),
        "relative_pass_rate_gain": round(
            adaptive_summary["pass_rate_60"] - random_summary["pass_rate_60"], 4
        ),
        "interaction_rows": adaptive_rows + random_rows,
        "learned_q_values": q_values[:40],
    }


def write_outputs(gkt_metrics: dict, q_metrics: dict, rows: list[dict]) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    synthetic_csv = OUTPUT_DIR / "synthetic_interactions.csv"
    fieldnames = sorted({key for row in rows for key in row.keys()})
    with synthetic_csv.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    q_csv = OUTPUT_DIR / "synthetic_q_learning_interactions.csv"
    with q_csv.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(q_metrics["interaction_rows"][0].keys()))
        writer.writeheader()
        writer.writerows(q_metrics["interaction_rows"])

    summary = {
        "metadata": {
            "random_seed": RANDOM_SEED,
            "student_count": 120,
            "module_count": len(MODULES),
            "subtopic_count": sum(len(items) for items in MODULES.values()),
            "data_type": "synthetic_simulation",
        },
        "neural_gkt_bootstrap": gkt_metrics,
        "q_learning": {
            key: value
            for key, value in q_metrics.items()
            if key not in {"interaction_rows"}
        },
        "files": {
            "synthetic_interactions": str(synthetic_csv.relative_to(ROOT)),
            "synthetic_q_learning_interactions": str(q_csv.relative_to(ROOT)),
        },
    }
    (OUTPUT_DIR / "metrics_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")


def main() -> None:
    rng = random.Random(RANDOM_SEED)
    students = build_students(rng)
    rows, pretest_state, _ = simulate_pretest_and_true_mastery(rng, students)
    gkt_metrics, rows = evaluate_neural_gkt_bootstrap(rng, students, rows, pretest_state)
    q_metrics = simulate_q_learning(students)
    write_outputs(gkt_metrics, q_metrics, rows)
    print(json.dumps({
        "neural_gkt_bootstrap": gkt_metrics,
        "q_learning": {
            "adaptive": q_metrics["adaptive"],
            "random_baseline": q_metrics["random_baseline"],
            "relative_mastery_gain": q_metrics["relative_mastery_gain"],
            "relative_pass_rate_gain": q_metrics["relative_pass_rate_gain"],
        },
    }, indent=2))


if __name__ == "__main__":
    main()
