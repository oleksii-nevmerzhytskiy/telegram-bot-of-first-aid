from abc import ABC, abstractmethod

from project.entities.user import User
from project.entities.user_state import UserState
from project.user.requests import ReceiveMassageRequest
from project.user.response import ReceiveMassageResponse, InitUserStateResponse, InitUserResponse


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

    @abstractmethod
    def init_user(self, chat_id: str) -> InitUserResponse:
        raise NotImplementedError




class IUserStateRepository(ABC):
    @abstractmethod
    def get_by_user_id(self, user_id: int) -> UserState:
        raise NotImplementedError

    @abstractmethod
    def save_user_state(self, user_state: UserState) -> UserState:
        raise NotImplementedError

class IUserStateUseCase(ABC):
    @abstractmethod
    def init_user_state(self, user_id: int) -> InitUserStateResponse:
        raise NotImplementedError