from abc import ABC, abstractmethod

from project.entities.decision_tree import DecisionTree
from project.entities.decision_tree_node import DecisionTreeNode






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

