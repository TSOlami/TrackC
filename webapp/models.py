from . import db
from flask_login import UserMixin
from sqlalchemy import *
import uuid
import secrets, os
from flask import url_for
from flask_mail import Message
from webapp import mail
from itsdangerous import URLSafeTimedSerializer as Serializer






class Transaction(db.Model):
    """ The Transaction Model """

    __tablename__ = 'transactions'
    id = db.Column(db.String(40), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String, db.ForeignKey('users.id'))
    coin_name = db.Column(db.String(30), nullable=False)
    symbol =  db.Column(db.String(30), nullable=False)
    price_purchased_at = db.Column(db.Numeric, nullable=False)
    amount_spent = db.Column(db.Numeric, nullable=False)
    no_of_coins = db.Column(db.Numeric, nullable=False)
    time_transacted = db.Column(db.DateTime(timezone=True), default=func.now())
    time_updated = db.Column(db.DateTime(timezone=True), default=func.now())

class User(db.Model, UserMixin):
    """The User Model"""

    __tablename__ = 'users'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(250), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    access = db.Column(db.Integer, nullable=False, default=1)
    transactions = db.relationship('Transaction', backref='user', lazy=True)
    portfolio_worth = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

    # Generate a password reset token
    def generate_reset_token(self, expires=1800):
        s = Serializer(os.environ['SECRET_KEY'])
        return s.dumps({'user_id': self.id})
    
    

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(os.environ['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

