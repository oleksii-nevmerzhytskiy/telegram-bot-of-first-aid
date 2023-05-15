from dataclasses import dataclass

from project.entities.decision_tree_node import DecisionTreeNode
from project.entities.status import Status


@dataclass
class DecisionTreeNodesResponse:

    step: str = ''
    nodes: [DecisionTreeNode] = None
    instruction: str = None
    image: str = None
    status: Status = None
