from dataclasses import dataclass
from enum import Enum
from project.entities.decision_tree_node import DecisionTreeNode
from project.entities.user_state import Module, UserState


class Status(Enum):
    OK = 1
    USER_DISABLED = 2
    ERROR = 3


@dataclass
class ReceiveMassageResponse:
    status: Status = None
    chat_id: str = None
    instruction: str = None
    image: str = None
    titles: [str] = None


@dataclass
class InitUserStateResponse:
    status: Status = None

@dataclass
class UpdateUserStateResponse:
    status: Status = None


@dataclass
class InitUserResponse:
    status: Status = None
    categories: [str] = None


@dataclass
class GetUserStateResponse:
    status: Status = None
    state: UserState = None


