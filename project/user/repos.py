
from project.entities.user import User
from app.models import UserModel as DjUser, UserStateModel as DjUserState
from project.entities.user_state import UserState, Module

from project.user.interfaces import IUserRepository, IUserStateRepository




class UserRepoFactory(object):
    @staticmethod
    def get() -> IUserRepository:
        return DjUserRepo()


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

class UserStateRepoFactory(object):
    @staticmethod
    def get() -> IUserStateRepository:
        return DjUserStateRepo()

class DjUserStateRepo(IUserStateRepository):

    def get_by_user_id(self, user_id: int) -> UserState:
        try:
            dj_user_state = DjUserState.objects.get(user_id=user_id)
        except DjUserState.DoesNotExist:
            return None  # todo
        return django_to_user_state(dj_user_state)

    def save_user_state(self, user_state: UserState) -> UserState:
        try:
            dj_user_state = user_state_to_django(user_state)
            dj_user_state.save()
        except DjUserState.DoesNotExist:
            return None  # todo
        return django_to_user_state(dj_user_state)


def django_to_user_state(dj_user_state:DjUserState) -> UserState:
    return UserState(id=dj_user_state.id,
                     user_id=dj_user_state.user.id,
                     module=Module(dj_user_state.module),
                     category=dj_user_state.category,
                     step=dj_user_state.step,
                     created_at=dj_user_state.created_at,
                     updated_at=dj_user_state.updated_at)

def user_state_to_django(user_state:UserState) -> DjUserState:
    return DjUserState(id=user_state.id,
                     user_id=user_state.user_id,
                     module=int(user_state.module),
                     category=user_state.category,
                     step=user_state.step,
                     created_at=user_state.created_at,
                     updated_at=user_state.updated_at)