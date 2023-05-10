from dataclasses import dataclass


@dataclass
class DecisionTreeNode:
    title: str = None
    step: str = None
    instruction: str = None
    image: str = None
    next_nodes: [] = None
