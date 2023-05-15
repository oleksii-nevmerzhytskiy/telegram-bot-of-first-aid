from dataclasses import dataclass
from datetime import datetime
from enum import IntEnum



class Module(IntEnum):
    INIT = 1
    DECISION_TREE = 2
    PLACES = 3
    ABOUT_BOT = 4


@dataclass
class UserState:
    id: int = None
    user_id: int = None
    module: Module = None
    category: str = ''
    step: str = ''
    created_at: datetime = None
    updated_at: datetime = None
