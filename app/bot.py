import os
import telebot

from project.user.response import Status
from project.user.usecase import UserUseCaseFactory

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'first_aid_bot.settings')
bot = telebot.TeleBot(os.getenv('BOT_SECRET_KEY'))


user_use_case = UserUseCaseFactory.get()


@bot.message_handler(commands=['start'])
def start(message):
    response = user_use_case.init_user(message.chat.id)
    print(response)
    if response.status is Status.OK:
        bot.send_message(message.chat.id, "Hello!!!")


def start_polling():
    bot.polling(none_stop=True)

