from project.entities.decision_tree import DecisionTree
from project.entities.decision_tree_node import DecisionTreeNode
from project.entities.user import User
from project.user.interfaces import IUserUseCase, IUserRepository, IDecisionUseCase, IDecisionTree
from project.user.requests import ReceiveMassageRequest
from project.user.response import ReceiveMassageResponse, Status


class UserUseCase(IUserUseCase):
    def __init__(self, repo: IUserRepository, d_use_case: IDecisionUseCase):
        self.repo = repo
        self.d_use_case = d_use_case



    def receive_message(self, req: ReceiveMassageRequest) -> ReceiveMassageResponse:
        resp = self.repo.get_by_chat_id(chat_id = req.chat_id)

        if resp is None:
            resp = self.repo.save_user(User(chat_id=req.chat_id, enabled=True))

        if not resp.enabled:
            return ReceiveMassageResponse(chat_id=req.chat_id, status=Status.USER_DISABLED)

        node = self.d_use_case.find_node_in_decision_tree('test_step3', req.massage)
        if node is None:
            return ReceiveMassageResponse(chat_id=req.chat_id, status=Status.ERROR)

        return ReceiveMassageResponse(chat_id=req.chat_id, status=Status.OK, node=node)


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
            node = n
            if n.step != step:
                node = self._find_node_in_decision_tree(step, title, node)

            if node is None:
                continue

            if node.next_nodes is None:
                return None

            for child in node.next_nodes:
                if child.title == title:
                    return child

            return None

        return None

    def find_node_in_decision_tree(self, step: str, title: str) -> DecisionTreeNode:
        tree = self.tree_repo.get_decision_tree()

        for node in tree.nodes:
            n = self._find_node_in_decision_tree(step, title, node)

            if n is not None:
                return n

        return None
