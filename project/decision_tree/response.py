from dataclasses import dataclass

from project.entities.decision_tree_node import DecisionTreeNode


@dataclass
class DecisionTreeNodesResponse:

    step: str = ''
    nodes: [DecisionTreeNode] = None
