import os

import telebot
from telebot import types
from flask import Flask, request, render_template, url_for
from flask_sqlalchemy import SQLAlchemy


TOKEN = '535439906:AAH3ZL2Yr64_lNnYEZlEepsPZXQoJyfr1S8'
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)
server.config.update({
    'SQLALCHEMY_DATABASE_URI': os.environ['DATABASE_URL'],
    'SQLALCHEMY_TRACK_MODIFICATIONS': False
})
db = SQLAlchemy(server)

class telegram_users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    is_bot = db.Column(db.Boolean)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    username = db.Column(db.String(100))
    language_code = db.Column(db.String(100))

    def __init__(self, id, is_bot, first_name, last_name, username, language_code):
        self.id = id
        self.is_bot = is_bot
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.language_code = language_code

    def __repr__(self):
        return '<telegram_users %r>' % self.id

db.create_all()

@bot.message_handler(commands=['start'])
def start(message):
    text = 'Greetings! Im Sunny SMM Robot! Send` /add ` to create new task. Want to know about all my options? Send` /help `and a list of the commands available for you will show up.`'
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row('Site', 'FAQ')
    bot.send_message(message.from_user.id, text, reply_markup=user_markup)

@bot.message_handler(commands=['add'])
def add(message):
    # telegram_user = telegram_users(message.from_user.id, message.from_user.is_bot, message.from_user.first_name,
    #                               message.from_user.last_name, message.from_user.username, message.from_user.language_code)
    # db.session.add(telegram_user)
    # db.session.commit()
    #admin = telegram_users(100, True, 'fdf', 'fdf', 'fdf', 'fdf')
    #db.session.add(admin)
    #db.session.commit()
    string_answer = "id: %s, is_bot: %s, first_name: %s, last_name: %s, username: %s, language_code: %s" % (message.from_user.id,
    message.from_user.is_bot, message.from_user.first_name, message.from_user.last_name, message.from_user.username,
    message.from_user.language_code)
    bot.send_message(message.from_user.id, string_answer)

@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return 'dsdsd', 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://sunnysmm.tk/' + TOKEN)
    return 'fdfdf!!!!', 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))