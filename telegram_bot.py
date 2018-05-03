#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

import telebot
from telebot import types
from flask import Flask, request, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from srcApp import instagram_api

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
    telegram_users_insta_accounts = db.relationship('telegram_users_insta_accounts', backref='telegram_users_insta_accounts', lazy=True)

    def __init__(self, id, is_bot=False, first_name='test', last_name='test', username='test', language_code='test'):
        self.id = id
        self.is_bot = is_bot
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.language_code = language_code

    def __repr__(self):
        return '<telegram_users %r>' % self.id

class telegram_users_insta_accounts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    telegram_id = db.Column(db.Integer, db.ForeignKey('telegram_users.id'), nullable=False)
    login = db.Column(db.String(100))
    password = db.Column(db.String(100))
    need_confirm_ip = db.Column(db.Boolean)

    def __init__(self, telegram_id):
        self.telegram_id = telegram_id

    def __repr__(self):
        return '<telegram_users %r>' % self.id


class conversation_line(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stage = db.Column(db.Integer, nullable=False)
    telegram_users_insta_account = db.Column(db.Integer, db.ForeignKey('telegram_users_insta_accounts.id'))
    language_code = db.Column(db.String(3))
    #0 - language
    #1 - empty
    #2 - wait login
    # 3 - wait password
    # 4 - wait insta check

    def __init__(self, telegram_id):
        self.id = telegram_id
        self.stage = 0

    def __repr__(self):
        return '<telegram_users %r>' % self.id

#db.drop_all()
db.create_all()

@bot.message_handler(commands=['start'])
def start(message):
    telegram_user = telegram_users.query.filter_by(id=message.from_user.id).first()
    if telegram_user == None:
        telegram_user = telegram_users(message.from_user.id)
        db.session.add(telegram_user)
        conversation = conversation_line(message.from_user.id)
        db.session.add(conversation)
        db.session.commit()

    conversation = conversation_line.query.filter_by(id=message.from_user.id).first()

    if conversation.stage == 0:
        text = 'Choose language:'
        keyboard = types.InlineKeyboardMarkup()
        callback_button1 = types.InlineKeyboardButton(text=u'\U0001F1F7\U0001F1FA' + ' Русский', callback_data="rus")
        #keyboard.add(callback_button)
        callback_button2 = types.InlineKeyboardButton(text=u'\U0001F1FA\U0001F1F8' + ' English', callback_data="eng")
        keyboard.row(callback_button1, callback_button2)
        #U+1F1F7 U+1F1FA
        #callback_button = types.InlineKeyboardButton(text=u'\U0001F1ECU0001F1E7', callback_data="eng")
        #keyboard.add(callback_button)
        bot.send_message(message.from_user.id, text, reply_markup=keyboard)
    elif conversation.language_code == 'rus':
        text = 'Русский Greetings! Im Sunny SMM Robot! Send` /instagram ` to set up instagram settings. Want to know about all my options?' \
               ' Send` /help `and a list of the commands available for you will show up.`'
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row('Site', 'FAQ')
        bot.send_message(message.from_user.id, text, reply_markup=user_markup)
    elif conversation.language_code == 'eng':
        text = 'Greetings! Im Sunny SMM Robot! Send` /instagram ` to set up instagram settings. Want to know about all my options?' \
               ' Send` /help `and a list of the commands available for you will show up.`'
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row('Site', 'FAQ')
        bot.send_message(message.from_user.id, text, reply_markup=user_markup)


@bot.message_handler(commands=['instagram'])
def instagram(message):

    conversation = conversation_line.query.filter_by(id=message.from_user.id).first()

    if conversation.language_code == 'rus':
        add_account_text = 'Добавить аккаунт'
        edit_account_text = 'Редактировать аккаунт: '
        instagram_setting_text = 'Добавьте или настройте инстаграм аккаунт:'
    else:
        add_account_text = 'New account'
        edit_account_text = 'Edit account: '
        instagram_setting_text = 'Edit or create new, instagram account:'

    # add inline buttons create new accounts
    keyboard = types.InlineKeyboardMarkup()
    callback_button = types.InlineKeyboardButton(add_account_text, callback_data="add_new")
    keyboard.add(callback_button)

    # seach allready exist instagram accounts
    insta_accounts = telegram_users_insta_accounts.query.filter_by(telegram_id=message.from_user.id).all()
    if insta_accounts == None:
        for insta_account in insta_accounts:
            callback_button = types.InlineKeyboardButton(text=edit_account_text + insta_account.login,
                                                         callback_data='edit_insta_account'+insta_account.id)
            keyboard.add(callback_button)

    bot.send_message(message.from_user.id, instagram_setting_text, reply_markup=keyboard)

@bot.message_handler(func=lambda message: True)
def all_messages(message):
	#bot.reply_to(message, message.text)

    bot.send_message(message.from_user.id, 'messages')

    conversation = conversation_line.query.filter_by(id=message.from_user.id).first()

    if conversation.language_code == 'rus':
        enter_password_text = "Введите password:"
        new_account_text = "Введите Instagram login:"
    else:
        enter_password_text = "Enter password:"
        new_account_text = "Enter instagram login:"

    if conversation.stage == 2:
        bot.send_message(message.from_user.id, 'stage2')
        if message.text != '':
            bot.send_message(message.from_user.id, 'stage2 not empty')
            db.session.query(telegram_users_insta_accounts).filter(telegram_users_insta_accounts.id == conversation.telegram_users_insta_account).update({'login': message.text})
            db.session.query(conversation_line).filter(conversation_line.id == message.from_user.id).update({'stage': 3})
            db.session.commit()
            bot.send_message(message.from_user.id, enter_password_text)
        else:
            bot.send_message(message.from_user.id, 'stage2 empty')
            bot.send_message(message.from_user.id, new_account_text)
    elif conversation.stage == 3:
        bot.send_message(message.from_user.id, 'stage3')
        if message.text != '':
            db.session.query(telegram_users_insta_accounts).filter(
                telegram_users_insta_accounts.id == conversation.telegram_users_insta_account).update(
                {'password': message.text})
            db.session.query(conversation_line).filter(conversation_line.id == message.from_user.id).update(
                {'stage': 3})
            db.session.commit()

            #telegram_users_insta_account = conversation_line.query.filter_by(id=message.from_user.id).first()

            #instagram_api.get_total_followers_direct_login(conversation.telegram_users_insta_account.login, 'Mitra123',
            #                                 'd0394ffe96:09de558d36@194.28.194.111:52593')

            #check insta acc

            bot.send_message(message.from_user.id, conversation.telegram_users_insta_account.login + ' fdfd ' + conversation.telegram_users_insta_account.password)
        else:
            bot.send_message(message.from_user.id, enter_password_text)


# В большинстве случаев целесообразно разбить этот хэндлер на несколько маленьких
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):

    # bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
    #                                text=call.from_user.id)
    # Если сообщение из чата с ботом
    bot.send_message(call.from_user.id, call.data[:17] + ' fdfdfd ' + call.data[18:])

    if call.message:
        if call.data == "add_new":
            #create dont have login stage 0
            conversation = conversation_line.query.filter_by(id=call.from_user.id).first()

            if conversation.language_code == 'rus':
                new_account_text = "Введите Instagram login:"

            else:
                new_account_text = "Enter instagram login:"

            if conversation.stage == 1:
                telegram_users_insta_account = telegram_users_insta_accounts(call.from_user.id)
                db.session.add(telegram_users_insta_account)
                db.session.commit()

                db.session.query(conversation_line).filter(conversation_line.id == call.from_user.id).update(
                    {'stage': 2, 'telegram_users_insta_account': telegram_users_insta_account.id})
                db.session.commit()

                #user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
                #user_markup.row('Site', 'FAQ')
                bot.send_message(call.from_user.id, new_account_text)

                # markup = types.ForceReply(selective=False)
                # bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                #                   text="Enter instagram login:" + call.from_user.id, reply_markup=markup)
        elif call.data[:17] == "edit_insta_account":
            fdfd=1
            # create dont have login stage 0
            # conversation = conversation_line.query.filter_by(id=call.from_user.id).first()
            #
            # if conversation.language_code == 'rus':
            #     new_account_text = "Введите Instagram login:"
            #
            # else:
            #     new_account_text = "Enter instagram login:"
            #
            # if conversation.stage == 1:
            #     telegram_users_insta_account = telegram_users_insta_accounts(call.from_user.id)
            #     db.session.add(telegram_users_insta_account)
            #     db.session.commit()
            #     # user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
            #     # user_markup.row('Site', 'FAQ')
            #     bot.send_message(call.from_user.id, new_account_text)
        elif call.data == "rus":
            text = 'Русский Greetings! Im Sunny SMM Robot! Send` /instagram ` to set up instagram settings. Want to know about all my options?' \
                   ' Send` /help `and a list of the commands available for you will show up.`'
            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
            user_markup.row('Site', 'FAQ')
            bot.send_message(call.from_user.id, text, reply_markup=user_markup)

            #conversation_line.update().where(id == call.from_user.id).values(dict(stage=1, language_code = 'rus'))
            db.session.query(conversation_line).filter(conversation_line.id == call.from_user.id).update(
                {'stage': 1, 'language_code': 'rus'})
            db.session.commit()

        elif call.data == 'eng':
            text = 'Greetings! Im Sunny SMM Robot! Send` /instagram ` to set up instagram settings. Want to know about all my options?' \
                   ' Send` /help `and a list of the commands available for you will show up.`'
            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
            user_markup.row('Site', 'FAQ')
            bot.send_message(call.from_user.id, text, reply_markup=user_markup)

            db.session.query(conversation_line).filter(conversation_line.id == call.from_user.id).update(
                {'stage': 1, 'language_code': 'eng'})
            db.session.commit()
            #conversation_line.update().where(id == call.from_user.id).values(dict(stage=1, language_code = 'eng'))



    # Если сообщение из инлайн-режима
    # elif call.inline_message_id:
    #     if call.data == "test":
    #         bot.edit_message_text(inline_message_id=call.inline_message_id, text="inline")

@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return 'dsdsd', 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://sunnysmm.tk/' + TOKEN)
    return 'telegram_users.query.all()[1].id', 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))