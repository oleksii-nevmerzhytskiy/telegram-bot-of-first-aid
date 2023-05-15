from dataclasses import dataclass


@dataclass
class DecisionTreeNode:
    id: int = None
    title: str = None
    step: str = None
    instruction: str = None
    image: str = None
    next_nodes: [] = None
