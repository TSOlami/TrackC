from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from sqlalchemy.orm import sessionmaker
import requests
from .models import *
views = Blueprint('views', __name__)

@views.route ('/')
def landing():
    return render_template("landing.html")

@views.route ('/home')
def home():
    return render_template("home.html", user=current_user)

@views.route('/transactions', methods=['POST','GET'])
def transactions():
    if request.method == 'POST':
        amount = request.form.get('amount')
        coin_name = request.form.get('coin_name')
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
