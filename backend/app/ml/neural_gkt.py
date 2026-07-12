from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path


MODEL_PATH = Path(__file__).resolve().parents[2] / "storage" / "neural_gkt_model.json"


def sigmoid(value: float) -> float:
    if value < -60:
        return 0.0
    if value > 60:
        return 1.0
    return 1.0 / (1.0 + math.exp(-value))


@dataclass
class NeuralGKTModel:
    """
    Lightweight trainable graph knowledge tracing model.

    The model keeps one hidden mastery probability per module node. A node state is
    predicted from the student's initial module signal and prerequisite messages:

    sigmoid(global_bias + node_bias + self_weight * initial_state
            + prerequisite_weight * avg(edge_weight * prerequisite_state))

    It intentionally avoids heavy ML dependencies so the project still runs on the
    current Python 3.13 setup. The training script can later be replaced by a
    PyTorch/DGL implementation without changing the backend inference contract.
    """

    node_ids: list[str] = field(default_factory=list)
    global_bias: float = 0.0
    self_weight: float = 2.0
    prerequisite_weight: float = 1.0
    node_bias: dict[str, float] = field(default_factory=dict)
    edge_weight: dict[str, float] = field(default_factory=dict)
    trained_samples: int = 0
    trained_at: str | None = None
    metrics: dict[str, float] = field(default_factory=dict)

    @property
    def is_trained(self) -> bool:
        return self.trained_samples > 0 and bool(self.node_ids)

    def edge_key(self, source_node_id: str, target_node_id: str) -> str:
        return f"{source_node_id}->{target_node_id}"

    def predict_states(
        self,
        initial_state: dict[str, float],
        prerequisites: dict[str, list[dict]],
        propagation_steps: int = 2,
    ) -> dict[str, float]:
        if not self.node_ids:
            return {}

        states = {
            node_id: min(1.0, max(0.0, initial_state.get(node_id, 0.0)))
            for node_id in self.node_ids
        }

        for _ in range(max(1, propagation_steps)):
            next_states: dict[str, float] = {}
            for node_id in self.node_ids:
                messages = []
                for prerequisite in prerequisites.get(node_id, []):
                    source_id = prerequisite["id"] if isinstance(prerequisite, dict) else prerequisite
                    weight = self.edge_weight.get(self.edge_key(source_id, node_id), 1.0)
                    messages.append(weight * states.get(source_id, initial_state.get(source_id, 0.0)))

                prerequisite_message = sum(messages) / len(messages) if messages else 0.0
                logit = (
                    self.global_bias
                    + self.node_bias.get(node_id, 0.0)
                    + self.self_weight * initial_state.get(node_id, states.get(node_id, 0.0))
                    + self.prerequisite_weight * prerequisite_message
                )
                next_states[node_id] = sigmoid(logit)
            states = next_states

        return states

    def evaluate_mastery(
        self,
        current_topic_id: str,
        initial_state: dict[str, float],
        prerequisites: dict[str, list[dict]],
        mastery_threshold: float = 0.6,
    ) -> dict:
        states = self.predict_states(initial_state=initial_state, prerequisites=prerequisites)
        if not states:
            return {
                "action": "continue",
                "recommended_topic": current_topic_id,
                "reason": "Model neural GKT belum memiliki state, gunakan graph prasyarat sebagai fallback.",
                "neural_state": {},
            }

        weak_prerequisite = self._find_weakest_prerequisite(
            current_topic_id=current_topic_id,
            states=states,
            prerequisites=prerequisites,
            mastery_threshold=mastery_threshold,
            visited=set(),
        )

        if weak_prerequisite:
            return {
                "action": "back_trace",
                "recommended_topic": weak_prerequisite,
                "reason": "Neural GKT memprediksi penguasaan prasyarat belum cukup kuat.",
                "neural_state": states,
            }

        return {
            "action": "continue",
            "recommended_topic": current_topic_id,
            "reason": "Neural GKT memprediksi prasyarat cukup untuk melanjutkan topik saat ini.",
            "neural_state": states,
        }

    def _find_weakest_prerequisite(
        self,
        current_topic_id: str,
        states: dict[str, float],
        prerequisites: dict[str, list[dict]],
        mastery_threshold: float,
        visited: set[str],
    ) -> str | None:
        if current_topic_id in visited:
            return None

        visited.add(current_topic_id)
        for prerequisite in prerequisites.get(current_topic_id, []):
            prerequisite_id = prerequisite["id"] if isinstance(prerequisite, dict) else prerequisite
            nested_gap = self._find_weakest_prerequisite(
                current_topic_id=prerequisite_id,
                states=states,
                prerequisites=prerequisites,
                mastery_threshold=mastery_threshold,
                visited=visited,
            )
            if nested_gap:
                return nested_gap

            if states.get(prerequisite_id, 0.0) < mastery_threshold:
                return prerequisite_id

        return None

    def to_dict(self) -> dict:
        return {
            "version": 1,
            "node_ids": self.node_ids,
            "global_bias": self.global_bias,
            "self_weight": self.self_weight,
            "prerequisite_weight": self.prerequisite_weight,
            "node_bias": self.node_bias,
            "edge_weight": self.edge_weight,
            "trained_samples": self.trained_samples,
            "trained_at": self.trained_at,
            "metrics": self.metrics,
        }

    @classmethod
    def from_dict(cls, payload: dict) -> "NeuralGKTModel":
        return cls(
            node_ids=list(payload.get("node_ids", [])),
            global_bias=float(payload.get("global_bias", 0.0)),
            self_weight=float(payload.get("self_weight", 2.0)),
            prerequisite_weight=float(payload.get("prerequisite_weight", 1.0)),
            node_bias={key: float(value) for key, value in payload.get("node_bias", {}).items()},
            edge_weight={key: float(value) for key, value in payload.get("edge_weight", {}).items()},
            trained_samples=int(payload.get("trained_samples", 0)),
            trained_at=payload.get("trained_at"),
            metrics={key: float(value) for key, value in payload.get("metrics", {}).items()},
        )

    def save(self, path: Path = MODEL_PATH) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        if not self.trained_at:
            self.trained_at = datetime.now(timezone.utc).isoformat()
        path.write_text(json.dumps(self.to_dict(), indent=2), encoding="utf-8")


def load_neural_gkt_model(path: Path = MODEL_PATH) -> NeuralGKTModel | None:
    if not path.exists():
        return None
    try:
        return NeuralGKTModel.from_dict(json.loads(path.read_text(encoding="utf-8")))
    except (json.JSONDecodeError, OSError, TypeError, ValueError):
        return None
