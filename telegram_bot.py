import os

import telebot
from telebot import types
from flask import Flask, request

TOKEN = '535439906:AAH3ZL2Yr64_lNnYEZlEepsPZXQoJyfr1S8'
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)
#keyboard = Keyboard(bot)


@bot.message_handler(commands=['start'])
def start(message):
    #bot.reply_to(message, 'Hello, ' + message.from_user.first_name)
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    #user_markup.row('Add instagram account')
    #user_markup.row('Change tasks')
    user_markup.row('Site', 'FAQ')
    bot.send_message(message.from_user.id, '', reply_markup=user_markup)

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*[types.InlineKeyboardButton(text = 'Add new account', callback_data = 'Add new account'), types.InlineKeyboardButton(text = 'Some1 else', callback_data = 'Some1 else')])

    bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=message.message_id,
        text='text',
        parse_mode='Markdown',
        reply_markup=keyboard)

@bot.message_handler(func=lambda mess: 'FAQ' == mess.text, content_types=['text'])
def handle_text(message):
    bot.send_message(message.from_user.id, 'To create new account use command fdfsgffgdg')
    #bot.reply_to(message, message.text)
    #UserPosition(database_url).set_getting_position(str(message.chat.id))
    #keyboard.get_all_faculties(message)

@bot.message_handler(func=lambda mess: 'Change tasks' == mess.text, content_types=['text'])
def handle_text(message):
    bot.send_message(message.from_user.id, 'Other messages')

@bot.message_handler(func=lambda mess: 'Site' == mess.text, content_types=['text'])
def default_test(message):
    keyboard = types.InlineKeyboardMarkup()
    url_button = types.InlineKeyboardButton(text="To the site", url="https://sunnysmm.tk")
    keyboard.add(url_button)
    bot.send_message(message.from_user.id, "Yo, push the button", reply_markup=keyboard)

@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.send_message(message.from_user.id, 'Other messages')


@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "sunny smm hello world", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://sunnysmm.tk/' + TOKEN)
    return "sunny smm hello world", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
