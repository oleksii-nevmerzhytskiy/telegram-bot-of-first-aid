from project.entities.decision_tree import DecisionTree
from project.entities.decision_tree_node import DecisionTreeNode
from project.entities.user import User
from app.models import UserModel as DjUser

from project.user.interfaces import IUserRepository, IDecisionTree


class DjUserRepo(IUserRepository):
    def get_by_chat_id(self, chat_id: str) -> User:
        try:
            dj_user = DjUser.objects.get(chat_id=chat_id)
        except DjUser.DoesNotExist:
            return None  # todo

        return django_to_user(dj_user)

    def save_user(self, user: User) -> User:
        try:
            dj_user = user_to_django(user)
            dj_user.save()
        except DjUser.DoesNotExist:
            return None  # todo
        return django_to_user(dj_user)


def django_to_user(dj_user: DjUser) -> User:
    return User(
        id=dj_user.id,
        chat_id=dj_user.chat_id,
        enabled=dj_user.enabled,
        created_at=dj_user.created_at,
        updated_at=dj_user.updated_at,
    )


def user_to_django(user: User) -> DjUser:
    return DjUser(
        id=user.id,
        chat_id=user.chat_id,
        enabled=user.enabled,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


class DjDecisionTree(IDecisionTree):
    def get_decision_tree(self) -> DecisionTree:
        return DecisionTree(nodes=[DecisionTreeNode(title="test3", step="test_step3", instruction="test_instruction3",
                                                    next_nodes=[DecisionTreeNode(title="test1", step="test_step1",
                                                                                 instruction="test_instruction1",
                                                                                 next_nodes=[
                                                                                     DecisionTreeNode(title="test5",
                                                                                                      step="test_step5",
                                                                                                      instruction="test_instruction5"),
                                                                                     DecisionTreeNode(title="test6",
                                                                                                      step="test_step6",
                                                                                                      instruction="test_instruction6")]),
                                                                DecisionTreeNode(title="test2", step="test_step2",
                                                                                 instruction="test_instruction2",
                                                                                 next_nodes=[
                                                                                     DecisionTreeNode(title="test7",
                                                                                                      step="test_step7",
                                                                                                      instruction="test_instruction7"),
                                                                                     DecisionTreeNode(title="test8",
                                                                                                      step="test_step8",
                                                                                                      instruction="test_instruction8")])])])
