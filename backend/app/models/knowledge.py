from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, UniqueConstraint, func
from sqlalchemy.orm import relationship

from app.core.database import Base


class KnowledgeState(Base):
    __tablename__ = "knowledge_states"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    node_id = Column(String, nullable=False, index=True)
    node_type = Column(String, nullable=False, default="subtopic")
    state_value = Column(Float, default=0.0)
    source = Column(String, default="manual")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User")

    __table_args__ = (
        UniqueConstraint("user_id", "node_id", "node_type", name="uq_user_knowledge_state"),
    )


class KnowledgeEdge(Base):
    __tablename__ = "knowledge_edges"

    id = Column(Integer, primary_key=True, index=True)
    source_node_id = Column(String, nullable=False, index=True)
    source_node_type = Column(String, nullable=False, default="module")
    target_node_id = Column(String, nullable=False, index=True)
    target_node_type = Column(String, nullable=False, default="module")
    relation_type = Column(String, nullable=False, default="prerequisite")
    weight = Column(Float, default=1.0)

    __table_args__ = (
        UniqueConstraint(
            "source_node_id",
            "source_node_type",
            "target_node_id",
            "target_node_type",
            "relation_type",
            name="uq_knowledge_edge",
        ),
    )
