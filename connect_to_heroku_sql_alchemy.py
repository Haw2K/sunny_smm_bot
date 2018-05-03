from flask import Flask, request, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

server = Flask(__name__)
server.config.update({
    'SQLALCHEMY_DATABASE_URI': "postgres://ilwxnlakhzsygl:1bb3b4c1078941d7c9cc0ec9a2df9e32c3989e3347149a259fdbd571ed51871b@ec2-107-21-103-146.compute-1.amazonaws.com:5432/demh6l5vnhecot",
    'SQLALCHEMY_TRACK_MODIFICATIONS': False
})
db = SQLAlchemy(server)
#from sqlalchemy import update

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

#        telegram_users_insta_account.update({'login': message.text})

#telegram_users_insta_account = db.session.query(telegram_users_insta_accounts).filter(telegram_users_insta_accounts.id == 1)
#telegram_users_insta_account.update({'login': 'test'})

id = 497327013

conversation = conversation_line.query.filter_by(id=id).first()

db.session.query(telegram_users_insta_accounts).filter(telegram_users_insta_accounts.id == conversation.telegram_users_insta_account).update({'login': 'haw22k'})
db.session.query(conversation_line).filter(conversation_line.id == id).update({'stage': 3})
db.session.commit()
#server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
#conversation_line.update().where(id == 497327013).values(dict(stage=1, language_code='rus'))
#    db.session.update(conversation_line).where(conversation_line.id == 5).values(dict(stage=1, language_code='rus'))
# db.session.commit()
# db.session.execute(update(conversation_line.where(conversation_line.id == 497327013).values(dict(stage=1, language_code='rus'))))
#db.session.commit()
#db.session.query(conversation_line).filter(conversation_line.id == 497327013).update({'stage': 1, 'language_code': 'rus'})
#db.session.commit()
# session.execute(update(stuff_table, values={stuff_table.c.foo: stuff_table.c.foo + 1}))
#  session.commit()
#conversation = conversation_line.query.filter_by(id=497327013).first()
fdfd=1