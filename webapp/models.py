from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import create_engine

engine = create_engine("postgresql://juuthoos:GaAe2ZbZU77KorqGd7NgIJKfm5Ya9EpH@dumbo.db.elephantsql.com/juuthoos")
Base = declarative_base()


class Transaction(Base):
    """Transaction Model"""
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime(timezone=True), default=func.now())
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    amount = Column(Float, nullable=False)

class User(Base, UserMixin):
    """The User Model"""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(250), unique=True, nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    transactions = relationship('Transaction', backref='user', lazy=True)