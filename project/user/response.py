from dataclasses import dataclass
from enum import Enum
from project.entities.decision_tree_node import DecisionTreeNode


class Status(Enum):
    OK = 1
    USER_DISABLED = 2
    ERROR = 3


@dataclass
class ReceiveMassageResponse:
    status: Status = None
    chat_id: str = None
    node: DecisionTreeNode = None


@dataclass
class InitUserStateResponse:
    status: Status = None


@dataclass
class InitUserResponse:
    status: Status = None

