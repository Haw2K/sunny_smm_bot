#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

import telebot
from telebot import types
from flask import Flask, request, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from srcApp import instagram_api
from sqlalchemy import update

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
    telegram_users_insta_accounts = db.Column(db.Integer, db.ForeignKey('telegram_users_insta_accounts.id'))
    language_code = db.Column(db.String(3))
    #0 - language
    #1 - add new instagram account
    #2 - add login
    # 3 - add password
    # 4 - change settings instagram account

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
        callback_button1 = types.InlineKeyboardButton(text=u'\U0001F1FA' + u'\U0001F1F8' + ' Русский', callback_data="rus")
        #keyboard.add(callback_button)
        callback_button2 = types.InlineKeyboardButton(text=u'\U0001F1F7\U0001F1FA' + ' English', callback_data="eng")
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
        #markup = types.ReplyKeyboardRemove(selective=False)
        #add inline buttons create new accounts
        keyboard = types.InlineKeyboardMarkup()
        callback_button = types.InlineKeyboardButton(text="Добавить аккаунт", callback_data="add_new")
        keyboard.add(callback_button)

        #seach allready exist instagram accounts
        insta_accounts = telegram_users_insta_accounts.query.filter_by(telegram_id = message.from_user.id).all()
        if insta_accounts == None:
            for insta_account in insta_accounts:
                callback_button = types.InlineKeyboardButton(text='Редактировать аккаунт: %s' % (insta_account.login), callback_data=insta_account.id)
                keyboard.add(callback_button)

        bot.send_message(message.from_user.id, 'Добавьте или настройте инстаграм аккаунт:', reply_markup=keyboard)
    else:
        # add inline buttons create new accounts
    keyboard = types.InlineKeyboardMarkup()
    callback_button = types.InlineKeyboardButton(text="Add new instagram account", callback_data="add_new")
    keyboard.add(callback_button)

    # seach allready exist instagram accounts
    insta_accounts = telegram_users_insta_accounts.query.filter_by(telegram_id=message.from_user.id).all()
    if insta_accounts == None:
        for insta_account in insta_accounts:
            callback_button = types.InlineKeyboardButton(text='Edit account: %s' % (insta_account.login),
                                                         callback_data=insta_account.id)
            keyboard.add(callback_button)

    bot.send_message(message.from_user.id, 'Edit or create new, instagram account:', reply_markup=keyboard)

        #'when we need confim we send you email'
        #instagram_api.get_total_followers_direct_login("nurtdinov.danil", 'Mitra123', 'd0394ffe96:09de558d36@194.28.194.111:52593')

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, message.text)

# В большинстве случаев целесообразно разбить этот хэндлер на несколько маленьких
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):

    # bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
    #                                text=call.from_user.id)
    # Если сообщение из чата с ботом
    if call.message:
        if call.data == "add_new":
            #create dont have login stage 0
            conversation = conversation_line.query.filter_by(id=call.from_user.id).first()

            telegram_users_insta_account_stage_0 = telegram_users_insta_accounts.query.filter_by(stage=0).first()
            telegram_users_insta_account_stage_1 = telegram_users_insta_accounts.query.filter_by(stage=1).first()
            if telegram_users_insta_account_stage_0 == None and telegram_users_insta_account_stage_1 == None:
                telegram_users_insta_account = telegram_users_insta_accounts(call.from_user.id)
                db.session.add(telegram_users_insta_account)
                db.session.commit()
                markup = types.ForceReply(selective=False)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Enter instagram login:" + call.from_user.id, reply_markup=markup)
        elif call.data == "rus":
            text = 'Русский Greetings! Im Sunny SMM Robot! Send` /instagram ` to set up instagram settings. Want to know about all my options?' \
                   ' Send` /help `and a list of the commands available for you will show up.`'
            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
            user_markup.row('Site', 'FAQ')
            bot.send_message(call.from_user.id, text, reply_markup=user_markup)

            conversation_line.update().where(id == call.from_user.id).values(stage=1)

        elif call.data == 'eng':
            text = 'Greetings! Im Sunny SMM Robot! Send` /instagram ` to set up instagram settings. Want to know about all my options?' \
                   ' Send` /help `and a list of the commands available for you will show up.`'
            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
            user_markup.row('Site', 'FAQ')
            bot.send_message(call.from_user.id, text, reply_markup=user_markup)

            conversation_line.update().where(id == call.from_user.id).values(stage=1)



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