from project.decision_tree.repos import DecisionTreeRepoFactory
from project.entities.decision_tree_node import DecisionTreeNode
from project.decision_tree.interfaces import IDecisionUseCase, IDecisionTree


class DecisionTreeUseCaseFactory(object):
    @staticmethod
    def get() -> IDecisionUseCase:
        return DecisionTreeUseCase(DecisionTreeRepoFactory.get())

class DecisionTreeUseCase(IDecisionUseCase):
    def __init__(self, tree_repo: IDecisionTree):
        self.tree_repo = tree_repo

    def _find_node_in_decision_tree(self, step: str, title: str, node: DecisionTreeNode) -> DecisionTreeNode:
        if node.step == step:
            if node.next_nodes is None:
                return None

            for child in node.next_nodes:
                if child.title == title:
                    return child
            return None

        if node.next_nodes is None:
            return None

        for n in node.next_nodes:
            node = self._find_node_in_decision_tree(step, title, n)

            if node is not None:
                return node

        return None

    def find_node_in_decision_tree(self, step: str, title: str) -> DecisionTreeNode:
        tree = self.tree_repo.get_decision_tree()

        for node in tree.nodes:
            n = self._find_node_in_decision_tree(step, title, node)

            if n is not None:
                return n

        return None
