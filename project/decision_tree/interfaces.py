from abc import ABC, abstractmethod

from project.decision_tree.response import DecisionTreeNodesResponse
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
    def get_decision_tree(self, category: str) -> DecisionTree:
        raise NotImplementedError

    def get_categories(self) -> [str]:
        raise NotImplementedError

class IDecisionUseCase(ABC):
    @abstractmethod
    def find_nodes_in_decision_tree(self, category: str, step: str, title: str) -> DecisionTreeNodesResponse:
        raise NotImplementedError

    @abstractmethod
    def get_categories(self) -> [str]:

        return NotImplementedError

