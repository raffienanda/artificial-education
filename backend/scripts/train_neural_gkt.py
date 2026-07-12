from __future__ import annotations

import argparse
import random
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core.database import SessionLocal
from app.ml.neural_gkt import MODEL_PATH, NeuralGKTModel, sigmoid
from app.models.assessment import AssessmentAttempt
from app.models.learning_path import TopicPrerequisite
from app.models.module import Module


def build_prerequisites(db) -> dict[str, list[dict]]:
    relations = db.query(TopicPrerequisite).all()
    if relations:
        graph: dict[str, list[dict]] = defaultdict(list)
        for relation in relations:
            graph[relation.topic_id].append({
                "id": relation.prerequisite_id,
                "mastery_threshold": (relation.mastery_threshold or 60.0) / 100.0,
            })
        return dict(graph)

    modules = db.query(Module).order_by(Module.order).all()
    return {
        modules[index].id: [{"id": modules[index - 1].id, "mastery_threshold": 0.6}]
        for index in range(1, len(modules))
    }


def fetch_real_samples(db) -> list[dict]:
    attempts = db.query(AssessmentAttempt).filter(
        AssessmentAttempt.assessment_type.in_(["pre_test", "post_test"]),
        AssessmentAttempt.finished_at.isnot(None),
    ).all()

    grouped: dict[tuple[int, str], dict[str, float]] = defaultdict(dict)
    for attempt in attempts:
        grouped[(attempt.user_id, attempt.module_id)][attempt.assessment_type] = (attempt.percentage or 0.0) / 100.0

    samples = []
    for (user_id, module_id), scores in grouped.items():
        if "pre_test" not in scores or "post_test" not in scores:
            continue
        samples.append({
            "user_id": user_id,
            "module_id": module_id,
            "initial": scores["pre_test"],
            "target": scores["post_test"],
            "source": "real",
        })
    return samples


def build_synthetic_samples(node_ids: list[str], prerequisites: dict[str, list[dict]], count: int = 240) -> list[dict]:
    rng = random.Random(42)
    samples = []
    ordered_nodes = list(node_ids)
    for student_id in range(count):
        latent_ability = rng.uniform(0.2, 0.9)
        module_state: dict[str, float] = {}
        for node_id in ordered_nodes:
            prereq_ids = [
                prerequisite["id"] if isinstance(prerequisite, dict) else prerequisite
                for prerequisite in prerequisites.get(node_id, [])
            ]
            prereq_mean = (
                sum(module_state.get(prereq_id, latent_ability) for prereq_id in prereq_ids) / len(prereq_ids)
                if prereq_ids
                else latent_ability
            )
            noise = rng.uniform(-0.12, 0.12)
            initial = min(1.0, max(0.0, latent_ability * 0.65 + prereq_mean * 0.25 + noise))
            target = min(1.0, max(0.0, initial * 0.45 + prereq_mean * 0.35 + latent_ability * 0.35 + rng.uniform(-0.08, 0.08)))
            module_state[node_id] = target
            samples.append({
                "user_id": -student_id,
                "module_id": node_id,
                "initial": initial,
                "target": target,
                "source": "synthetic",
            })
    return samples


def train_model(
    node_ids: list[str],
    prerequisites: dict[str, list[dict]],
    samples: list[dict],
    epochs: int = 600,
    learning_rate: float = 0.04,
) -> NeuralGKTModel:
    model = NeuralGKTModel(
        node_ids=node_ids,
        global_bias=-0.2,
        self_weight=2.0,
        prerequisite_weight=1.0,
        node_bias={node_id: 0.0 for node_id in node_ids},
        edge_weight={
            f"{prerequisite['id'] if isinstance(prerequisite, dict) else prerequisite}->{node_id}": 1.0
            for node_id, prereqs in prerequisites.items()
            for prerequisite in prereqs
        },
    )

    for _ in range(epochs):
        random.shuffle(samples)
        for sample in samples:
            node_id = sample["module_id"]
            initial = sample["initial"]
            target = sample["target"]
            prereqs = prerequisites.get(node_id, [])
            prereq_initials = []
            for prerequisite in prereqs:
                prerequisite_id = prerequisite["id"] if isinstance(prerequisite, dict) else prerequisite
                prereq_samples = [
                    item["target"]
                    for item in samples
                    if item["user_id"] == sample["user_id"] and item["module_id"] == prerequisite_id
                ]
                prereq_initials.append(prereq_samples[-1] if prereq_samples else initial)

            edge_messages = []
            edge_keys = []
            for index, prerequisite in enumerate(prereqs):
                prerequisite_id = prerequisite["id"] if isinstance(prerequisite, dict) else prerequisite
                edge_key = model.edge_key(prerequisite_id, node_id)
                edge_keys.append(edge_key)
                edge_messages.append(model.edge_weight.get(edge_key, 1.0) * prereq_initials[index])

            prereq_message = sum(edge_messages) / len(edge_messages) if edge_messages else 0.0
            logit = (
                model.global_bias
                + model.node_bias.get(node_id, 0.0)
                + model.self_weight * initial
                + model.prerequisite_weight * prereq_message
            )
            prediction = sigmoid(logit)
            error = prediction - target
            gradient = error * prediction * (1.0 - prediction)

            model.global_bias -= learning_rate * gradient
            model.node_bias[node_id] = model.node_bias.get(node_id, 0.0) - learning_rate * gradient
            model.self_weight -= learning_rate * gradient * initial
            model.prerequisite_weight -= learning_rate * gradient * prereq_message

            for edge_key, prereq_value in zip(edge_keys, prereq_initials):
                edge_gradient = gradient * model.prerequisite_weight * prereq_value / max(1, len(edge_keys))
                model.edge_weight[edge_key] = model.edge_weight.get(edge_key, 1.0) - learning_rate * edge_gradient

    squared_error = 0.0
    absolute_error = 0.0
    correct = 0
    for sample in samples:
        prediction = model.predict_states(
            initial_state={sample["module_id"]: sample["initial"]},
            prerequisites=prerequisites,
            propagation_steps=1,
        ).get(sample["module_id"], 0.0)
        target = sample["target"]
        squared_error += (prediction - target) ** 2
        absolute_error += abs(prediction - target)
        correct += int((prediction >= 0.6) == (target >= 0.6))

    total = max(1, len(samples))
    model.trained_samples = len(samples)
    model.trained_at = datetime.now(timezone.utc).isoformat()
    model.metrics = {
        "mae": round(absolute_error / total, 4),
        "rmse": round((squared_error / total) ** 0.5, 4),
        "accuracy_at_60": round(correct / total, 4),
        "real_samples": sum(1 for item in samples if item["source"] == "real"),
        "synthetic_samples": sum(1 for item in samples if item["source"] == "synthetic"),
    }
    return model


def main() -> None:
    parser = argparse.ArgumentParser(description="Train lightweight Neural GKT model from assessment data.")
    parser.add_argument("--min-real-samples", type=int, default=30)
    parser.add_argument("--epochs", type=int, default=600)
    parser.add_argument("--learning-rate", type=float, default=0.04)
    parser.add_argument("--no-synthetic", action="store_true")
    args = parser.parse_args()

    db = SessionLocal()
    try:
        modules = db.query(Module).order_by(Module.order).all()
        node_ids = [module.id for module in modules]
        prerequisites = build_prerequisites(db)
        samples = fetch_real_samples(db)

        if len(samples) < args.min_real_samples and not args.no_synthetic:
            samples.extend(build_synthetic_samples(node_ids=node_ids, prerequisites=prerequisites))

        if not samples:
            raise SystemExit("Tidak ada sample training. Jalankan pre/post test dulu atau hapus --no-synthetic.")

        model = train_model(
            node_ids=node_ids,
            prerequisites=prerequisites,
            samples=samples,
            epochs=args.epochs,
            learning_rate=args.learning_rate,
        )
        model.save(MODEL_PATH)

        print({
            "saved_to": str(MODEL_PATH),
            "trained_samples": model.trained_samples,
            "metrics": model.metrics,
            "trained_at": model.trained_at,
        })
    finally:
        db.close()


if __name__ == "__main__":
    main()
