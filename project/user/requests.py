from dataclasses import dataclass

@dataclass
class ReceiveMassageRequest:
    massage: str = None
    chat_id: str = None


