import os

import telebot
from flask import Flask, request

TOKEN = '535439906:AAH3ZL2Yr64_lNnYEZlEepsPZXQoJyfr1S8'
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)
keyboard = Keyboard(bot)


@bot.message_handler(commands=['start'])
def start(message):
    #bot.reply_to(message, 'Hello, ' + message.from_user.first_name)
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row('Add instagram account')
    user_markup.row('Change tasks')
    user_markup.row('Site', 'FAQ')
    bot.send_message(message.from_user.id, 'Select menu item:', reply_markup=user_markup)

@bot.message_handler(func=lambda mess: 'Add instagram account' == mess.text, content_types=['text'])
def handle_text(message):
    bot.send_message(message.from_user.id, 'Database new account')
    #bot.reply_to(message, message.text)
    #UserPosition(database_url).set_getting_position(str(message.chat.id))
    #keyboard.get_all_faculties(message)

@bot.message_handler(func=lambda mess: 'Change tasks' == mess.text, content_types=['text'])
def handle_text(message):
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
