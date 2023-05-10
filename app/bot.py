import os
import telebot

from project.decision_tree.repos import DjDecisionTree
from project.decision_tree.usecase import DecisionTreeUseCase
from project.user.repos import DjUserRepo, DjUserStateRepo
from project.user.requests import ReceiveMassageRequest
from project.user.response import Status
from project.user.usecase import UserUseCase, UserStateUseCase

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'first_aid_bot.settings')
bot = telebot.TeleBot(os.getenv('BOT_SECRET_KEY'))

user_repo = DjUserRepo()
decision_tree_repo = DjDecisionTree()
decision_tree_use_case = DecisionTreeUseCase(decision_tree_repo)

user_state_repo = DjUserStateRepo()
user_state_use_case = UserStateUseCase(user_state_repo)

user_use_case = UserUseCase(user_repo, decision_tree_use_case, user_state_use_case)


@bot.message_handler(commands=['start'])
def start(message):
    response = user_use_case.init_user(message.chat.id)
    print(response)
    if response.status is Status.OK:
        bot.send_message(message.chat.id, "Hello!!!")


def start_polling():
    bot.polling(none_stop=True)

