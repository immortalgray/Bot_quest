from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from telebot.types import Message
from telebot import TeleBot
from function import load_data, save_user_data, make_keyboard
from config import token


bot = TeleBot(token=token)


data_quest = load_data('data_quest.json')
user_data = load_data('user_data.json')


@bot.message_handler(commands=['start'])
def begin(massage: Message):
    user_id = str(massage.from_user.id)
    if user_id not in user_data or user_data[user_id]["location"] == '':
        user_data[user_id] = {"name": massage.from_user.first_name,
                              "location": ''}
        save_user_data(user_data)
        keyboard_start = make_keyboard(data_quest["Вернуться в начала"]["options"])
        with open(f'media/{data_quest["Вернуться в начала"]["location"]}.png', 'rb') as file:
            bot.send_photo(massage.chat.id, photo=file, caption=f'{data_quest["Вернуться в начала"]["description"]}',
                           reply_markup=keyboard_start)
    else:
        kb_continue = ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = KeyboardButton('Продолжить')
        btn2 = KeyboardButton('Начать сначала')
        kb_continue.add(btn1, btn2)
        bot.send_message(massage.from_user.id, f'Приветствую тебя {massage.from_user.first_name}, '
                                               f'продолжим или начнём сначала?', reply_markup=kb_continue)


@bot.message_handler(content_types=['text'])
def quest(message: Message):
    user_id = str(message.from_user.id)
    if message.text == 'Продолжить':
        loc = user_data[user_id]["location"]
        keyboard = make_keyboard(data_quest[loc]["options"])
        with open(f'media/{data_quest[loc]["location"]}.png', 'rb') as file:
            bot.send_photo(message.from_user.id, photo=file,
                           caption=f'{data_quest[loc]["description"]}',
                           reply_markup=keyboard)
    elif message.text == 'Начать сначала':
        user_data[user_id]["location"] = ''
        save_user_data(user_data)
        keyboard_start = make_keyboard(data_quest["Вернуться в начала"]["options"])
        with open(f'media/{data_quest["Вернуться в начала"]["location"]}.png', 'rb') as file:
            bot.send_photo(message.chat.id, photo=file, caption=f'{data_quest["Вернуться в начала"]["description"]}',
                           reply_markup=keyboard_start)
    else:
        if message.text in data_quest:
            buttons = data_quest[message.text]["options"]
            if buttons:
                keyboard = make_keyboard(buttons)
            else:
                keyboard = make_keyboard(['Начать сначала'])
            with open(f'media/{data_quest[message.text]["location"]}.png', 'rb') as file:
                bot.send_photo(message.from_user.id, photo=file,
                               caption=f'{data_quest[message.text]["description"]}',
                               reply_markup=keyboard)
            user_data[user_id]["location"] = message.text
            save_user_data(user_data)
        else:
            bot.send_message(message.from_user.id, 'Вы ошиблись, воспользуйтесь клавиатурой.')


bot.infinity_polling()
