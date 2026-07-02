class GraphKnowledgeTracing:
    """
    Macro-layer tracing over topic prerequisites.
    This version uses the persisted prerequisite graph and mastery scores.
    """

    def __init__(self, mastery_threshold: float = 60.0):
        self.mastery_threshold = mastery_threshold

    def evaluate_mastery(
        self,
        current_topic_id: str,
        topic_mastery: dict[str, float],
        prerequisites: dict[str, list],
    ) -> dict:
        weak_prerequisite = self._find_weakest_prerequisite(
            current_topic_id=current_topic_id,
            topic_mastery=topic_mastery,
            prerequisites=prerequisites,
            visited=set(),
        )

        if weak_prerequisite:
            return {
                "action": "back_trace",
                "recommended_topic": weak_prerequisite,
                "reason": "Topik prasyarat belum cukup kuat untuk melanjutkan learning path.",
            }

        return {
            "action": "continue",
            "recommended_topic": current_topic_id,
            "reason": "Penguasaan prasyarat cukup untuk melanjutkan topik saat ini.",
        }

    def _find_weakest_prerequisite(
        self,
        current_topic_id: str,
        topic_mastery: dict[str, float],
        prerequisites: dict[str, list],
        visited: set[str],
    ) -> str | None:
        if current_topic_id in visited:
            return None

        visited.add(current_topic_id)
        direct_prerequisites = prerequisites.get(current_topic_id, [])

        for prerequisite in direct_prerequisites:
            if isinstance(prerequisite, dict):
                prerequisite_id = prerequisite["id"]
                threshold = prerequisite.get("mastery_threshold", self.mastery_threshold)
            else:
                prerequisite_id = prerequisite
                threshold = self.mastery_threshold

            nested_gap = self._find_weakest_prerequisite(
                current_topic_id=prerequisite_id,
                topic_mastery=topic_mastery,
                prerequisites=prerequisites,
                visited=visited,
            )
            if nested_gap:
                return nested_gap

            mastery = topic_mastery.get(prerequisite_id, 0.0)
            if mastery < threshold:
                return prerequisite_id

        return None


gkt_model = GraphKnowledgeTracing()
