import os
import telebot
from telebot import types

from project.entities.status import Status
from project.entities.user_state import Module
from project.user.requests import ReceiveMassageRequest
from project.user.usecase import UserUseCaseFactory
from django.utils.translation import gettext as _

LOCATION = {}
CONTENT_TYPES = ["audio", "document", "photo", "sticker", "video", "video_note", "voice", "contact",
                 "new_chat_members", "left_chat_member", "new_chat_title", "new_chat_photo", "delete_chat_photo",
                 "group_chat_created", "supergroup_chat_created", "channel_chat_created", "migrate_to_chat_id",
                 "migrate_from_chat_id", "pinned_message"]

places_btn_value = _('Search for the nearest medical facilities')
about_btn_value = _('About the project')
back_to_reality = _('Back to reality')
main = _('Main')
send_location = _('send_location')
hospital_btn_value = _('hospital')
pharmacy_btn_value = _('pharmacy')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'first_aid_bot.settings')
bot = telebot.TeleBot(os.getenv('BOT_SECRET_KEY'))

user_use_case = UserUseCaseFactory.get()
user_use_case.set_commands_messages(places_btn_value, about_btn_value, hospital_btn_value, pharmacy_btn_value)
callback_data = ''


def create_keyboard(titles: [str]):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
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
    # itembtn1 = types.KeyboardButton(back_to_reality)
    itembtn2 = types.KeyboardButton(main)
    # markup.add(itembtn1, itembtn2)
    markup.add(itembtn2)
    return markup


def add_main_button(markup):
    itembtn1 = types.KeyboardButton(main)
    markup.add(itembtn1)
    return markup


def create_service_keyboard():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    # itembtn1 = types.KeyboardButton(back_to_reality)
    itembtn2 = types.KeyboardButton(main)
    # markup.add(itembtn1, itembtn2)
    markup.add(itembtn2)
    return markup


def create_places_keyboard():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    itembtn = types.KeyboardButton(send_location, request_location=True)
    markup.add(itembtn)

    return markup


@bot.message_handler(commands=['start'])
def start(message):
    response = user_use_case.init_user(message.chat.id)

    if response.status is Status.OK:
        bot.send_message(message.chat.id, _("Welcome message"),
                         reply_markup=add_modules_keyboard(create_keyboard(response.categories)))
    else:
        bot.send_message(message.chat.id, _("Use the buttons or restart the bot (/start)"))


@bot.message_handler(commands=['help'])
def help(message):
    response = user_use_case.init_user(message.chat.id)

    if response.status is Status.OK:
        bot.send_message(message.chat.id, _("Help message"))
    else:
        bot.send_message(message.chat.id, _("Use the buttons or restart the bot (/start)"))


@bot.message_handler(content_types=['text'])
def handle_message(message):
    global places_btn_value
    global about_btn_value
    global main

    if message.text == places_btn_value:
        bot.send_message(message.chat.id, _('click the "Share location" button'),
                         reply_markup=add_main_button(create_places_keyboard()))
        return
    elif message.text == about_btn_value:

        text = _('about bot message')
        bot.send_message(message.chat.id, text,
                         reply_markup=(create_service_keyboard()))
        return
    elif message.text == main:
        start(message)
        return

    chat_id = message.chat.id
    if chat_id in (LOCATION.keys()):
        longitude = LOCATION[chat_id]['longitude']
        latitude = LOCATION[chat_id]['latitude']
    else:
        longitude = latitude = ''
    resp = user_use_case.receive_message(
        ReceiveMassageRequest(massage=message.text, chat_id=chat_id, longitude=longitude, latitude=latitude))

    if resp.status == Status.ERROR:
        bot.send_message(message.chat.id, _("Use the buttons or restart the bot (/start)"))
        return
    if resp.module == Module.PLACES:
        handle_places(resp, message)
        return
    if resp.module == Module.DECISION_TREE:
        handle_decision_tree(resp, message)
        return


def handle_decision_tree(resp, message):
    str_image = str(resp.image)
    if not str_image == '':
        photo_file = open(str_image, 'rb')
        bot.send_photo(message.chat.id, photo_file)
        photo_file.close()
    titles = resp.titles
    if len(titles) == 0:
        bot.send_message(message.chat.id, resp.instruction, reply_markup=create_service_keyboard())
        return

    bot.send_message(message.chat.id, resp.instruction, reply_markup=add_service_keyboard(create_keyboard(titles)))


@bot.message_handler(content_types=['location'])
def accept_location(message):
    global LOCATION
    resp = user_use_case.receive_message(ReceiveMassageRequest(massage=places_btn_value, chat_id=message.chat.id))
    bot.send_message(message.chat.id, _("select the institution type"),
                     reply_markup=add_service_keyboard(create_keyboard(resp.titles)))
    LOCATION[message.chat.id] = {'longitude': message.location.longitude, 'latitude': message.location.latitude}


def handle_places(resp, message):
    markup = types.InlineKeyboardMarkup()

    for place in resp.places:
        callback = str(place.longitude) + ' ' + str(place.latitude)
        markup.add(
            types.InlineKeyboardButton(place.place_address + ", " + place.place_name, callback_data=callback))
    bot.send_message(message.chat.id, _("Select an address to view details"), reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def places_callback_query(call: telebot.types.CallbackQuery):
    f: telebot.types.InlineKeyboardButton = None
    for l in call.message.reply_markup.keyboard:
        for v in l:
            if v.callback_data == call.data:
                f = v
                break

    longitude, latitude = call.data.split(' ')
    if f is not None:
        bot.send_message(call.message.chat.id, text=f.text, reply_to_message_id=call.message.id)
    bot.send_location(call.message.chat.id, longitude=longitude, latitude=latitude)


@bot.message_handler(content_types=CONTENT_TYPES)
def fallback(message):
    bot.send_message(message.chat.id, _("Use the buttons or restart the bot (/start)"))


def start_polling():
    bot.polling(none_stop=True)
