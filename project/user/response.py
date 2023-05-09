from dataclasses import dataclass
from enum import Enum

class Status(Enum):
    OK = 1
    USER_DISABLED = 2
    ERROR = 3



@dataclass
class ReceiveMassageResponse:
    status: Status = None
    chat_id: str = None
