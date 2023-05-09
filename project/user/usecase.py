from project.entities.user import User
from project.user.interfaces import IUserUseCase, IUserRepository
from project.user.requests import ReceiveMassageRequest
from project.user.response import ReceiveMassageResponse, Status


class UserUseCase(IUserUseCase):
    def __init__(self, repo: IUserRepository):
        self.repo = repo



    def receive_message(self, req: ReceiveMassageRequest) -> ReceiveMassageResponse:
        resp = self.repo.get_by_chat_id(chat_id = req.chat_id)

        if resp is None:
            resp = self.repo.save_user(User(chat_id=req.chat_id, enabled=True))

        if not resp.enabled:
            return ReceiveMassageResponse(chat_id=req.chat_id, status=Status.USER_DISABLED)

        return ReceiveMassageResponse(chat_id=req.chat_id, status=Status.OK)
