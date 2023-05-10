from abc import ABC, abstractmethod

from project.entities.decision_tree import DecisionTree
from project.entities.decision_tree_node import DecisionTreeNode
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


class IDecisionTree(ABC):
    # @abstractmethod
    # def create_decision_tree(self, decision_tree_node: DecisionTreeNode) -> DecisionTree:
    #     raise NotImplementedError
    #
    # @abstractmethod
    # def update_decision_tree(self, decision_tree: DecisionTree) -> DecisionTree:
    #     raise NotImplementedError
    #
    # @abstractmethod
    # def find_decision_tree(self, decision_tree: DecisionTree) -> DecisionTreeNode:
    #     raise NotImplementedError
    # @abstractmethod
    # def find_in_decision_tree(self, title: str, decision_tree: DecisionTree) -> DecisionTreeNode:
    #     raise NotImplementedError
    @abstractmethod
    def get_decision_tree(self) -> DecisionTree:
        raise NotImplementedError

class IDecisionUseCase(ABC):
    @abstractmethod
    def find_node_in_decision_tree(self, step: str, title: str) -> DecisionTreeNode:
        raise NotImplementedError
