import os
import telebot


from project.user.repos import DjUser, DjUserRepo
from project.user.requests import ReceiveMassageRequest
from project.user.response import Status
from project.user.usecase import UserUseCase


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'first_aid_bot.settings')
bot = telebot.TeleBot(os.getenv('BOT_SECRET_KEY'))

user_repo = DjUserRepo()
user_use_case = UserUseCase(user_repo)

@bot.message_handler()
def start(message):
    print(message)
    response = user_use_case.receive_message(ReceiveMassageRequest(message.text, message.chat.id))
    print(response)
    if response.status is Status.OK:
        bot.send_message(message.chat.id, "Hello!!!")


def start_polling():
    bot.polling(none_stop=True)

