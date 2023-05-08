from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    id: int = None
    chat_id: str = None
    enabled: bool = None
    created_at: datetime = None
    updated_at: datetime = None
