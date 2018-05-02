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
#keyboard = Keyboard(bot)

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True)
#     email = db.Column(db.String(120), unique=True)
#
#     def __init__(self, username, email):
#         self.username = username
#         self.email = email
#
#     def __repr__(self):
#         return '<User %r>' % self.username

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



# return '<User %r>' % self.username

    #addresses = db.relationship('Address', backref='person',
    #                           lazy='dynamic')

db.create_all()

#
#
# class Address(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(50))
#     person_id = db.Column(db.Integer, db.ForeignKey('person.id'))



@bot.message_handler(commands=['start'])
def start(message):
    text = 'Greetings! Im Sunny SMM Robot! Send` /add ` to create new task. Want to know about all my options? Send` /help `and a list of the commands available for you will show up.`'
    #bot.reply_to(message, 'Hello, ' + message.from_user.first_name)
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    #user_markup.row('Add instagram account')
    #user_markup.row('Change tasks')
    user_markup.row('Site', 'FAQ')
    bot.send_message(message.from_user.id, text, reply_markup=user_markup)

    #keyboard = types.InlineKeyboardMarkup()
    #keyboard.add(*[types.InlineKeyboardButton(text = 'Add new account', callback_data = 'Add new account'), types.InlineKeyboardButton(text = 'Some1 else', callback_data = 'Some1 else')])

    #bot.edit_message_text(        chat_id=message.chat.id,        message_id=message.message_id,        text='text',        parse_mode='Markdown')
        #reply_markup=keyboard)

@bot.message_handler(commands=['add'])
def start(message):
    telegram_user = telegram_users(message.from_user.id, message.from_user.is_bot, message.from_user.first_name,
                                   message.from_user.last_name, message.from_user.username, message.from_user.language_code)
    db.session.add(telegram_user)
    db.session.commit()
    bot.send_message(message.from_user.id, 'all right')

# # Handle '/start' and '/help'
# @bot.message_handler(commands=['help', 'start'])
# def send_welcome(message):
#     msg = bot.reply_to(message, """\
# Hi there, I am Example bot.
# What's your name?
# """)
#     bot.register_next_step_handler(msg, process_name_step)
#
#
# def process_name_step(message):
#     try:
#         chat_id = message.chat.id
#         name = message.text
#         user = User(name)
#         user_dict[chat_id] = user
#         msg = bot.reply_to(message, 'How old are you?')
#         bot.register_next_step_handler(msg, process_age_step)
#     except Exception as e:
#         bot.reply_to(message, 'oooops')

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
    return telegram_users.query.all()[0].id, 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://sunnysmm.tk/' + TOKEN)
    return telegram_users.query.all()[0].id, 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))