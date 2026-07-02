from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class QLearningConfig:
    alpha: float = 0.1
    gamma: float = 0.9
    mastery_pass_threshold: float = 80.0


class QLearningAgent:
    """
    Micro-layer agent for selecting the next subtopic intervention.
    The Q-table is persisted in the database; this class only owns the policy math.
    """

    ACTIONS = ("show_text", "show_video", "easy_quiz", "hard_quiz", "review_previous")

    def __init__(self, config: QLearningConfig | None = None):
        self.config = config or QLearningConfig()

    def build_state(self, mastery: float, recent_failures: int = 0) -> str:
        if mastery >= 80:
            mastery_bucket = "high"
        elif mastery >= 50:
            mastery_bucket = "medium"
        else:
            mastery_bucket = "low"

        if recent_failures >= 2:
            failure_bucket = "stuck"
        elif recent_failures == 1:
            failure_bucket = "retry"
        else:
            failure_bucket = "stable"

        return f"{mastery_bucket}:{failure_bucket}"

    def select_action(self, q_values: dict[str, float], allowed_actions: Iterable[str] | None = None) -> str:
        actions = tuple(allowed_actions or self.ACTIONS)
        if not actions:
            return "show_text"

        return max(actions, key=lambda action: (q_values.get(action, 0.0), -actions.index(action)))

    def calculate_reward(self, is_correct: bool, mastery_before: float, mastery_after: float, first_attempt: bool = True) -> float:
        reward = 100.0 if is_correct and first_attempt else 35.0 if is_correct else -10.0
        reward += max(-20.0, min(20.0, mastery_after - mastery_before))

        if mastery_after >= self.config.mastery_pass_threshold and mastery_before < self.config.mastery_pass_threshold:
            reward += 25.0

        return reward

    def update_q_value(self, current_q: float, reward: float, next_max_q: float) -> float:
        return current_q + self.config.alpha * (
            reward + self.config.gamma * next_max_q - current_q
        )


q_agent = QLearningAgent()
