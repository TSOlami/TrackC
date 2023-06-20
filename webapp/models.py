from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy import *
import sqlalchemy.orm
from sqlalchemy.orm import relationship


engine = create_engine("postgresql://juuthoos:GaAe2ZbZU77KorqGd7NgIJKfm5Ya9EpH@dumbo.db.elephantsql.com/juuthoos")
Base = sqlalchemy.orm.declarative_base()

class Transaction(Base):
    """ The Transaction Model """

    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    date = Column(DateTime(timezone=True), default=func.now())
    amount = Column(Float, nullable=False)
    coin_name = Column(String(30), nullable=False)
    price_purchased_at = Column(Numeric, nullable=False)
    no_of_coins = Column(Numeric, nullable=False)

class User(Base, UserMixin):
    """The User Model"""

    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(250), unique=True, nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    access = Column(Integer, nullable=False, default=1)
    transactions = relationship('Transaction', backref='user', lazy=True)
