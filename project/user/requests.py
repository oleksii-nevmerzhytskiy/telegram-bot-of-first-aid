from dataclasses import dataclass

from project.entities.user_state import Module


@dataclass
class ReceiveMassageRequest:
    massage: str = None
    chat_id: str = None
    longitude: str = ''
    latitude: str = ''

@dataclass
class UpdateUserStateRequest:
    user_id: int = None
    module: Module = None
    category: str = None
    step: str = None


