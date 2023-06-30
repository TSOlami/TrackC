from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy import *
import sqlalchemy.orm
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

db = SQLAlchemy()

class Transaction(db.Model):
    """ The Transaction Model """

    __tablename__ = 'transactions'
    id = db.Column(db.String(40), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String, db.ForeignKey('users.id'))
    coin_name = db.Column(db.String(30), nullable=False)
    symbol =  db.Column(db.String(30), nullable=False)
    price_purchased_at = db.Column(db.Numeric, nullable=False)
    amount = db.Column(db.Numeric, nullable=False)
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
    transaction_type = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
