import os
import telebot
from dotenv import load_dotenv

load_dotenv()

bot = telebot.TeleBot(os.getenv('SECRET_KEY'))

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f"{message.from_user.first_name} {message.from_user.last_name} hello!!!")


bot.polling(none_stop=True)