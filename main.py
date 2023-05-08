import os
import telebot
from dotenv import load_dotenv

load_dotenv()

bot = telebot.TeleBot(os.getenv('BOT_SECRET_KEY'))

@bot.message_handler(commands=['start'])
def start(message):
    print(message)
    bot.send_message(message.chat.id, "[+380684794539](+380684794539)", parse_mode="Markdown")



bot.polling(none_stop=True)