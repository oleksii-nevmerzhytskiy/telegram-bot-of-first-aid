from abc import ABC, abstractmethod

from project.entities.user import User


class IUserRepository(ABC):
    @abstractmethod
    def get_chat_id(self, chat_id: str) -> User:
        raise NotImplementedError

    @abstractmethod
    def save_user(self, user: User) -> User:
        raise NotImplementedError
