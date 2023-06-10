from dataclasses import dataclass

from project.entities.place import Place
from project.entities.status import Status
from project.entities.user_state import UserState, Module


@dataclass
class ReceiveMassageResponse:
    status: Status = None
    chat_id: str = None
    instruction: str = ''
    image: str = ''
    titles: [str] = None
    module: Module = None
    places: [Place] = None


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


