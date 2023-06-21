import datetime
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from sqlalchemy.orm import sessionmaker
import requests
from .models import *
views = Blueprint('views', __name__)

@views.route ('/')
def landing():
    return render_template("landing.html")

@views.route ('/home/')
def home():
    user_id = request.args.get('user_id')
    return render_template("home.html", user_id=user_id)

@views.route('/<user_id>/transactions', methods=['GET'])
def transactions(user_id):
    coin_name_list = []
    amount_list = []
    symbol_list = []
    price_purchased_at_list = []
    no_of_coins_list = []
    time_transacted_list = []
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    for trans in session.query(Transaction).all():
        if trans.user_id == user_id:
           coin_name_list.append(trans.coin_name)
           amount_list.append(trans.amount)
           symbol_list.append(trans.symbol)
           price_purchased_at_list.append(trans.price_purchased_at)
           no_of_coins_list.append(trans.no_of_coins)
           time_transacted_list.append(trans.time_transacted)
    if coin_name_list is None:
        session.cloe()
        return "None"
    else:
        return render_template('transactions.html', coin_name_list=coin_name_list, amount_list=amount_list, symbol_list=symbol_list, price_purchased_at_list=price_purchased_at_list, no_of_coins_list=no_of_coins_list, time_transacted_list=time_transacted_list)

@views.route('/<user_id>/transactions', methods=['POST'])
def new_transactions(user_id):
    if request.method == 'POST':
        coin_name = request.form.get('coin_name')
        coin_name = coin_name.lower()
        amount = request.form.get('amount')
        amount = request.form.get('amount')
        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
        api_key = "05bf26b5-a99a-4eb7-92f4-e2c8bc263693"
        headers = {'Accepts' : 'application/json', 'X-CMC_PRO_API_KEY' : api_key}
        params = { 'start' : '1', 'limit' : '5000', 'convert' : 'USD'}
        data = requests.get(url, params=params, headers=headers).json()
        for i in range(0, 5000):
            if data['data'][i]['name'].lower() == coin_name:
                price_purchased_at = data['data'][i]['quote']['USD']['price']
                no_of_coins = float(amount) / price_purchased_at
                symbol = data['data'][i]['symbol']
                Base.metadata.create_all(engine)
                Session = sessionmaker(bind=engine)
                session = Session()
                user_id = user_id
                for trans in session.query(Transaction).all():
                    if trans.coin_name.lower() == coin_name and trans.user_id == user_id:
                         trans.amount = float(amount) + float(trans.amount)
                         trans.no_of_coins = float(trans.no_of_coins) + (float(amount) / price_purchased_at)
                         session.commit()
                         session.close()
                         return "Transaction Updated"                         
                new_trans = Transaction(user_id=user_id, amount=amount, coin_name=coin_name.capitalize(), symbol=symbol, price_purchased_at=price_purchased_at, no_of_coins=no_of_coins)
                session.add(new_trans)
                session.commit()
                session.close()
                return "Transaction Added!"
        return "Unable to add Transaction"
#@views.route('/transactions/<transaction_id>', methods=['PUT'])
#def update_transactions(transaction_id):
    
