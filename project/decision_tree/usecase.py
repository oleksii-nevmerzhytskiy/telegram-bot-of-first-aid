from project.decision_tree.repos import DecisionTreeRepoFactory
from project.decision_tree.response import DecisionTreeNodesResponse
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

    def find_nodes_in_decision_tree(self, category: str, step: str, title: str) -> DecisionTreeNodesResponse:
        tree = self.tree_repo.get_decision_tree(category)
        if step == '' and title is None:
            return DecisionTreeNodesResponse(nodes=tree.nodes, instruction=tree.instruction, image=tree.image)

        if step == '':
            for n in tree.nodes:
                if n.title == title:
                    if n.next_nodes is not None:
                        return DecisionTreeNodesResponse(nodes=n.next_nodes, step=n.step, instruction=n.instruction, image=n.image)
                    else:
                        return DecisionTreeNodesResponse(nodes=[], step='', instruction=n.instruction, image=n.image)

            return DecisionTreeNodesResponse(nodes=None)



        for node in tree.nodes:
            n = self._find_node_in_decision_tree(step, title, node)
            print(n)
            if n is not None:
               if n.next_nodes is not None:
                   return DecisionTreeNodesResponse(nodes=n.next_nodes, step=n.step, instruction=n.instruction, image=n.image)
               else:
                   return DecisionTreeNodesResponse(nodes=[], step=n.step, instruction=n.instruction, image=n.image)

        return DecisionTreeNodesResponse(nodes=None) # todo

    def get_categories(self) -> [str]:
        return self.tree_repo.get_categories()



