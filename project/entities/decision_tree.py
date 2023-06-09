from dataclasses import dataclass
from datetime import datetime

from project.entities.decision_tree_node import DecisionTreeNode


@dataclass
class DecisionTree:
    id: int = None
    category: str = None
    instruction: str = None
    image: str = None
    nodes: [DecisionTreeNode] = None
    created_at: datetime = None
    updated_at: datetime = None

