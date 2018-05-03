from flask import Flask, request, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

server = Flask(__name__)
server.config.update({
    'SQLALCHEMY_DATABASE_URI': "postgres://ilwxnlakhzsygl:1bb3b4c1078941d7c9cc0ec9a2df9e32c3989e3347149a259fdbd571ed51871b@ec2-107-21-103-146.compute-1.amazonaws.com:5432/demh6l5vnhecot",
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
    #0 - start
    #1 - add new instagram account
    #2 - add login
    # 3 - add password
    # 4 - change settings instagram account

    def __init__(self, telegram_id):
        self.id = telegram_id
        self.stage = 0

    def __repr__(self):
        return '<telegram_users %r>' % self.id

db.drop_all()
db.create_all()

if __name__ == "__main__":
    #server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
    telegram_user = telegram_users.query.all()
    telegram_users_insta_account_stage_0 = telegram_users_insta_accounts.query.all()
        #filter_by(stage=0).first()
    fdfd=1