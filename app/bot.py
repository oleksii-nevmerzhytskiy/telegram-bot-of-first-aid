import os
import telebot
from telebot import types

from project.entities.status import Status
from project.user.requests import ReceiveMassageRequest
from project.user.usecase import UserUseCaseFactory
from django.utils.translation import gettext as _

CONTENT_TYPES = ["audio", "document", "photo", "sticker", "video", "video_note", "voice", "contact",
                 "new_chat_members", "left_chat_member", "new_chat_title", "new_chat_photo", "delete_chat_photo",
                 "group_chat_created", "supergroup_chat_created", "channel_chat_created", "migrate_to_chat_id",
                 "migrate_from_chat_id", "pinned_message"]

places_btn_value = _('Search for the nearest medical facilities')
about_btn_value = _('About the project')
back_to_reality = _('Back to reality')
main = _('Main')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'first_aid_bot.settings')
bot = telebot.TeleBot(os.getenv('BOT_SECRET_KEY'))


user_use_case = UserUseCaseFactory.get()

def create_keyboard(titles: [str]):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn = []
    for category in titles:
        itembtn.append(types.KeyboardButton(category))
        if len(itembtn) == 2:
            markup.add(itembtn[0], itembtn[1])
            itembtn = []

    if len(itembtn) > 0:
        markup.add(itembtn[0])

    return markup

def add_modules_keyboard(markup):
    itembtn1 = types.KeyboardButton(places_btn_value)
    itembtn2 = types.KeyboardButton(about_btn_value)
    markup.add(itembtn1, itembtn2)
    return markup

def add_service_keyboard(markup):
    itembtn1 = types.KeyboardButton(back_to_reality)
    itembtn2 = types.KeyboardButton(main)
    markup.add(itembtn1, itembtn2)
    return markup
def create_service_keyboard():
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton(back_to_reality)
    itembtn2 = types.KeyboardButton(main)
    markup.add(itembtn1, itembtn2)
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    response = user_use_case.init_user(message.chat.id)

    if response.status is Status.OK:
        bot.send_message(message.chat.id, _("Welcome message"), reply_markup=add_service_keyboard(add_modules_keyboard(create_keyboard(response.categories))))


@bot.message_handler(content_types=['text'])
def handle_message(message):
    global places_btn_value
    global about_btn_value
    global main

    if message.text == places_btn_value:
        pass
    elif message.text == about_btn_value:
        pass
    elif message.text == main:
        start(message)
        return

    resp = user_use_case.receive_message(ReceiveMassageRequest(massage=message.text, chat_id=message.chat.id))

    if resp.status == Status.ERROR:
        bot.send_message(message.chat.id, _("Use the buttons or restart the bot (/start)"))
        return
    str_image = str(resp.image)
    if not str_image == '':
        photo_file = open(str_image, 'rb')
        bot.send_photo(message.chat.id, photo_file)
        photo_file.close()
    titles = resp.titles
    if titles is None:
        bot.send_message(message.chat.id, resp.instruction, reply_markup=create_service_keyboard())
        return

    bot.send_message(message.chat.id, resp.instruction, reply_markup=add_service_keyboard(create_keyboard(titles)))



@bot.message_handler(content_types=CONTENT_TYPES)
def fallback(message):
    bot.send_message(message.chat.id, _("Use the buttons or restart the bot (/start)"))


def start_polling():
    bot.polling(none_stop=True)

