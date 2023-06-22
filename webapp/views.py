import datetime
import json
from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy.orm import sessionmaker
import requests
from requests.exceptions import RequestException, ConnectionError, Timeout, TooManyRedirects
from .models import *
from datetime import datetime
from newsapi import NewsApiClient

views = Blueprint('views', __name__)


@views.route ('/')
def landing():
    return render_template("landing.html")


@views.route ('/home/')
def home():
    # Endpoint to get top 10 crytpo-currencies from CMC
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {'start':'1', 
                  'limit':'10', 
                  'convert':'USD'}
    headers = {'Accepts': 'application/json', 
               'X-CMC_PRO_API_KEY': 
               '05bf26b5-a99a-4eb7-92f4-e2c8bc263693'}
    # Create a new transaction
    session = requests.Session()
    session.headers.update(headers)

    response = session.get(url, params=parameters)
    data = json.loads(response.text)
    results = data['data']
    # Loop through the results
    for result in results:
        result['quote']['USD']['price'] = '$ ' + "{:.2f}".format(result['quote']['USD']['price'])
    #Render results on the homepage
    user_id = request.args.get('user_id')
    return render_template("home.html", user_id=user_id, results=results)


@views.route ('/news')
def news():
    # Endpoint to make NewsApi calls
    newsapi = NewsApiClient(api_key="1877e2279f07408189ec7af252270bf8")
    topheadlines = newsapi.get_top_headlines(sources="al-jazeera-english")
    articles = topheadlines['articles']

    desc = []
    news = []
    img = []

    for i in range (len(articles)):
        allarticles = articles[i]

        news.append(allarticles['title'])
        desc.append(allarticles['description'])
        img.append(allarticles['urlToImage'])
    # Archive the list 
    mylist = zip(news, desc, img)
    print(mylist)
    return render_template("news.html", context=mylist)


@views.route ('/hottests')
def get_top_10():
    pass


@views.route('/<user_id>/transactions/add_transaction', methods=['POST'])
def new_transactions(user_id):
    """Endpoint to add a new transaction"""

    # Retrieve form data from the frontend
    coin_name = request.form.get('coin_name')
    coin_name = coin_name.lower()
    amount = request.form.get('amount')

    # Setup CoinMarketCap API 
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    api_key = "05bf26b5-a99a-4eb7-92f4-e2c8bc263693"
    headers = {'Accepts': 'application/json', 'X-CMC_PRO_API_KEY': api_key}
    params = {'start': '1', 'limit': '5000', 'convert': 'USD'}
    data = requests.get(url, params=params, headers=headers).json()

    # Find the cryptocurrency matching the provided name
    for i in range(0, 5000):
        if data['data'][i]['name'].lower() == coin_name:
            price_purchased_at = data['data'][i]['quote']['USD']['price']
            no_of_coins = float(amount) / price_purchased_at
            symbol = data['data'][i]['symbol']

            # Create a database session
            Base.metadata.create_all(engine)
            Session = sessionmaker(bind=engine)
            session = Session()

            user_id = user_id

            # Check if the transaction already exists for the user and coin
            for trans in session.query(Transaction).all():
                if trans.coin_name.lower() == coin_name and trans.user_id == user_id:
                    # Update the existing transaction
                    trans.amount = float(amount) + float(trans.amount)
                    trans.no_of_coins = float(trans.no_of_coins) + (float(amount) / price_purchased_at)
                    trans.time_updated = datetime.now()
                    portfolio_worth = float(session.query(User).get(user_id).portfolio_worth) + float(amount)
                    session.query(User).get(user_id).portfolio_worth = portfolio_worth
                    session.commit()
                    session.close()
                    return redirect(url_for("views.transactions", user_id=user_id))

            # Create a new transaction
            portfolio_worth = float(session.query(User).get(user_id).portfolio_worth) + float(amount)
            new_trans = Transaction(user_id=user_id, 
                                    amount=amount, 
                                    coin_name=coin_name.capitalize(),
                                    symbol=symbol, 
                                    price_purchased_at=price_purchased_at, 
                                    no_of_coins=no_of_coins)
            
            session.query(User).get(user_id).portfolio_worth = portfolio_worth
            session.add(new_trans)
            session.commit()
            session.close()
            return redirect(url_for("views.transactions", user_id=user_id))

    # If no matching cryptocurrency found
    return "Unable to add Transaction"


@views.route('/<user_id>/transactions', methods=['GET'])
def transactions(user_id):
    """Endpoint to fetch data from the database"""
    coin_name_list = []
    amount_list = []
    symbol_list = []
    price_purchased_at_list = []
    no_of_coins_list = []
    time_transacted_list = []
    time_updated_list = []
    # Create a new transaction
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    for trans in session.query(Transaction).all():
        if trans.user_id == user_id:
           coin_name_list.append(trans.coin_name)
           amount_list.append(trans.amount)
           symbol_list.append(trans.symbol)
           price_purchased_at_list.append(trans.price_purchased_at)
           url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
           api_key = "05bf26b5-a99a-4eb7-92f4-e2c8bc263693"
           headers = {'Accepts' : 'application/json', 'X-CMC_PRO_API_KEY' : api_key}
           params = { 'start' : '1', 'limit' : '5000', 'convert' : 'USD'}
           data = requests.get(url, params=params, headers=headers).json()
           for i in range(0, 5000):
               if data['data'][i]['name'].lower() == trans.coin_name.lower():
                   no_of_coins = float(trans.amount) / data['data'][i]['quote']['USD']['price']
                   no_of_coins_list.append(no_of_coins)
                   time_transacted_list.append(trans.time_transacted)
                   time_updated_list.append(trans.time_updated)
    portfolio_worth = sum(amount_list)
    session.query(User).get(user_id).portfolio_worth = portfolio_worth
    return render_template('transactions.html', 
                           user_id=user_id, 
                           coin_name_list=coin_name_list, 
                           amount_list=amount_list, 
                           symbol_list=symbol_list, 
                           price_purchased_at_list=price_purchased_at_list, 
                           no_of_coins_list=no_of_coins_list, 
                           time_transacted_list=time_transacted_list, 
                           time_updated_list=time_updated_list, 
                           portfolio_worth=portfolio_worth
                           )


@views.route('/<user_id>/transactions/update_transaction', methods=['POST'])
def update_transactions(user_id):
    """Endpoint to update a transaction"""
    coin_name = request.form.get('coin_name')
    coin_name = coin_name.lower()
    amount = request.form.get('amount')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    for trans in session.query(Transaction).all():
        if trans.coin_name.lower() == coin_name and trans.user_id == user_id:
            url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
            api_key = "05bf26b5-a99a-4eb7-92f4-e2c8bc263693"
            headers = {'Accepts' : 'application/json', 'X-CMC_PRO_API_KEY' : api_key}
            params = { 'start' : '1', 'limit' : '5000', 'convert' : 'USD'}
            data = requests.get(url, params=params, headers=headers).json()
            for i in range(0, 5000):
                if data['data'][i]['name'].lower() == coin_name:
                    price_purchased_at = data['data'][i]['quote']['USD']['price']
                    trans.amount = float(amount) + float(trans.amount)
                    trans.no_of_coins = float(trans.no_of_coins) + (float(amount) / price_purchased_at)
                    trans.time_updated = datetime.now()
                    portfolio_worth = float(session.query(User).get(user_id).portfolio_worth) + float(amount)
                    session.query(User).get(user_id).portfolio_worth = portfolio_worth
                    session.commit()
                    session.close()
                    return redirect(url_for("views.transactions", user_id=user_id))
    return "Coin is not pressent in your portfolio"



