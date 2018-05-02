from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


class telegram_users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    is_bot = db.Column(db.Boolean)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    username = db.Column(db.String(100))
    language_code = db.Column(db.String(100))

    def __init__(self, id, is_bot=False, first_name='test', last_name='test', username='test', language_code='test'):
        self.id = id
        self.is_bot = is_bot
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.language_code = language_code

    def __repr__(self):
        return '<telegram_users %r>' % self.id

db.create_all()
#from yourapplication import User
admin = telegram_users(103)
db.session.add(admin)
db.session.commit()
dd = telegram_users.query.all()

user = telegram_users.query.filter_by(id='102').first()

fdf =1