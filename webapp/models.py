from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy import *
import sqlalchemy.orm
from sqlalchemy.orm import relationship
import uuid

engine = create_engine("postgresql://juuthoos:GaAe2ZbZU77KorqGd7NgIJKfm5Ya9EpH@dumbo.db.elephantsql.com/juuthoos")
Base = sqlalchemy.orm.declarative_base()


class Transaction(Base):
    """ The Transaction Model """

    __tablename__ = 'transactions'
    id = Column(String(40), primary_key=True,  default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey('users.id'))
    coin_name = Column(String(30), nullable=False)
    symbol =  Column(String(30), nullable=False)
    price_purchased_at = Column(Numeric, nullable=False)
    amount = Column(Float, nullable=False)
    no_of_coins = Column(Numeric, nullable=False)
    time_transacted = Column(DateTime(timezone=True), default=func.current_timestamp())
    time_updated = Column(DateTime(timezone=True), default=func.now())

class User(Base, UserMixin):
    """The User Model"""

    __tablename__ = 'users'
    id = Column(String(36), primary_key=True,  default=lambda: str(uuid.uuid4()))
    username = Column(String(250), unique=True, nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    access = Column(Integer, nullable=False, default=1)
    transactions = relationship('Transaction', backref='user', lazy=True)
    net_worth =  Column(Float, default=0)
    date_created = Column(DateTime(timezone=True), default=func.now())

Base.metadata.create_all(engine)
