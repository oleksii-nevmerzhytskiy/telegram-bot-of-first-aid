from project.entities.user import User
from app.models import UserModel as DjUser

from project.user.interfaces import IUserRepository

class DjUserRepo(IUserRepository):
    def get_by_chat_id(self, chat_id: str) -> User:
        try:
            dj_user = DjUser.objects.get(chat_id = chat_id)
        except DjUser.DoesNotExist:
            return None # todo

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