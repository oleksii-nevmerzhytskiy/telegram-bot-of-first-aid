from abc import ABC, abstractmethod

from project.entities.user import User
from project.user.requests import ReceiveMassageRequest
from project.user.response import ReceiveMassageResponse


class IUserRepository(ABC):
    @abstractmethod
    def get_by_chat_id(self, chat_id: str) -> User:
        raise NotImplementedError

    @abstractmethod
    def save_user(self, user: User) -> User:
        raise NotImplementedError


class IUserUseCase(ABC):
    @abstractmethod
    def receive_message(self, req: ReceiveMassageRequest) -> ReceiveMassageResponse:
        raise NotImplementedError
