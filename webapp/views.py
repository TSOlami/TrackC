import datetime
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from sqlalchemy.orm import sessionmaker
import requests
from .models import *
views = Blueprint('views', __name__)

@views.route ('/')
def landing():
    return "This is the landing page"
    # return render_template("landing.html")

@views.route ('/home')
def home():
    return render_template("home.html", user=current_user)

@views.route('/transactions', methods=['GET','POST'])
def new_transactions():
    if request.method == 'POST':
        coin_name = request.json["coin_name"]
        amount = request.json["amount"]
        trans_type = request.json["trans_type"]
        time_transacted = datetime.fromtimestamp(request.json["time_transacted"])
        price_purchased_at = float(request.json["price_purchased_at"])
        time_created = datetime.fromtimestamp(request.json["time_created"])
        no_of_coins = float(request.json["no_of_coins"])
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        new_trans = Transaction(coin_name=coin_name, amount=amount, trans_type=trans_type, time_transacted=time_transacted, price_purchased_at=price_purchased_at, time_created=time_created, no_of_coins=no_of_coins)
        session.add(new_trans)
        return jsonify(request.json)

        coin_name = coin_name.lower()
        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
        api_key = "05bf26b5-a99a-4eb7-92f4-e2c8bc263693"
        headers = {'Accepts' : 'application/json', 'X-CMC_PRO_API_KEY' : api_key}
        params = { 'start' : '1', 'limit' : '5000', 'convert' : 'USD'}
        data = requests.get(url, params=params, headers=headers).json()
        for i in range(0, 5000):
            if data['data'][i]['name'].lower() == coin_name:
                price_purchased_at = data['data'][i]['quote']['USD']['price']
                no_of_coins = int(amount) / price_purchased_at
                Base.metadata.create_all(engine)
                Session = sessionmaker(bind=engine)
                session = Session()
                new_trans = Transaction(amount=amount, coin_name=coin_name, price_purchased_at=price_purchased_at, no_of_coins=no_of_coins)
                session.add(new_trans)
                return "Transaction Added!"
        return "Unable to add Transaction"
    return render_template('transactions.html')
