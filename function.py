import json
from telebot.types import KeyboardButton, ReplyKeyboardMarkup


def load_data(data):
    try:
        with open(data, 'r+', encoding='utf8') as f:
            return json.load(f)
    except:
        return {}


def save_user_data(user_data):
    with open('user_data.json', 'w+', encoding='utf8') as f:
        json.dump(user_data, f, ensure_ascii=False, indent=4)


def make_keyboard(options):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for ell in options:
        keyboard.add(KeyboardButton(ell))
    return keyboard
