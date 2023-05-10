from project.decision_tree.interfaces import IDecisionUseCase
from project.decision_tree.usecase import DecisionTreeUseCaseFactory
from project.entities.user import User
from project.entities.user_state import UserState
from project.user.interfaces import IUserUseCase, IUserRepository, IUserStateUseCase, IUserStateRepository
from project.user.repos import UserRepoFactory, UserStateRepoFactory
from project.user.requests import ReceiveMassageRequest
from project.user.response import ReceiveMassageResponse, Status, InitUserStateResponse, InitUserResponse
from project.entities.user_state import Module

class UserUseCaseFactory(object):
    @staticmethod
    def get() -> IUserUseCase:
        return UserUseCase(UserRepoFactory.get(), DecisionTreeUseCaseFactory.get(), UserStateUseCaseFactory.get())

class UserUseCase(IUserUseCase):
    def __init__(self, repo: IUserRepository, decision_tree_use_case: IDecisionUseCase, user_state_use_case: IUserStateUseCase):
        self.repo = repo
        self.decision_tree_use_case = decision_tree_use_case
        self.user_state_use_case = user_state_use_case

    def init_user(self, chat_id: str) -> InitUserResponse:
        resp = self.repo.get_by_chat_id(chat_id=chat_id)

        if resp is None:
            resp = self.repo.save_user(User(chat_id=chat_id, enabled=True))

        if resp is None:
            return InitUserResponse(status=Status.ERROR)

        if not resp.enabled:
            return InitUserResponse(status=Status.USER_DISABLED)
        status_resp = self.user_state_use_case.init_user_state(resp.id)

        if status_resp.status == Status.ERROR:
            return InitUserResponse(status=Status.ERROR)

        return InitUserResponse(status=Status.OK)

    def receive_message(self, req: ReceiveMassageRequest) -> ReceiveMassageResponse:
        resp = self.repo.get_by_chat_id(chat_id = req.chat_id)

        if resp is None:
            resp = self.repo.save_user(User(chat_id=req.chat_id, enabled=True))

        if not resp.enabled:
            return ReceiveMassageResponse(chat_id=req.chat_id, status=Status.USER_DISABLED)

        node = self.decision_tree_use_case.find_node_in_decision_tree('test_step3', req.massage)
        if node is None:
            return ReceiveMassageResponse(chat_id=req.chat_id, status=Status.ERROR)

        return ReceiveMassageResponse(chat_id=req.chat_id, status=Status.OK, node=node)


class UserStateUseCaseFactory(object):
    @staticmethod
    def get() -> IUserStateUseCase:
        return UserStateUseCase(UserStateRepoFactory.get())

class UserStateUseCase(IUserStateUseCase):
    def __init__(self, repo: IUserStateRepository):
        self.repo = repo

    def init_user_state(self, user_id: int) -> InitUserStateResponse:
        state = self.repo.get_by_user_id(user_id=user_id)

        if state is None:
            state = UserState(user_id=user_id, module=Module.INIT)
        else:
            state.module = Module.INIT
            state.step = ''
            state.category = ''
        state = self.repo.save_user_state(state)

        if state is None:
            return InitUserStateResponse(status=Status.ERROR)

        return InitUserStateResponse(status=Status.OK)
