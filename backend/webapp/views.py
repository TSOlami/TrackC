import datetime
import json
from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import login_required, current_user
from sqlalchemy.orm import sessionmaker
import requests
from requests.exceptions import RequestException, ConnectionError, Timeout, TooManyRedirects
from .models import *
from datetime import datetime
#from newsapi import NewsApiClient
from newsapi.newsapi_client import NewsApiClient


views = Blueprint('views', __name__)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

@views.route ('/')
def landing():
    return render_template("landing.html")


@views.route('/home/<user_id>')
def home(user_id):
    # Endpoint to get top 10 cryptocurrencies from CMC
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'start': '1',
        'limit': '10',
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': '05bf26b5-a99a-4eb7-92f4-e2c8bc263693'
    }
    # Create a db session
    session = requests.Session()
    session.headers.update(headers)
    
    response = session.get(url, params=parameters)
    data = json.loads(response.text)
    results = data['data']

    for result in results:
        result['quote']['USD']['price'] = '$ ' + "{:.2f}".format(result['quote']['USD']['price'])
        result['quote']['USD']['volume_24h'] = '$ ' + "{:.2f}".format(result['quote']['USD']['volume_24h'])
        result['quote']['USD']['percent_change_24h'] = "{:.2f}".format(result['quote']['USD']['percent_change_24h']) + '%'

    # Retrieve user-specific data based on the user_id parameter
    # ... Add your code here to fetch user-specific data ...

    return jsonify({'user_id': user_id, 'results': results})


@views.route ('/news')
def news():
    # Endpoint to make NewsApi calls
    news_url = "https://api.coingecko.com/api/v3/news"
    formatted_data = get_formatted_news_data(news_url)
    return render_template('news.html', news=formatted_data)

def get_formatted_news_data(news_url):
    response = requests.get(news_url)
    data = response.json()
    formatted_data = format_data(data)
    return formatted_data

def format_data(data):
    formatted_data = []
    for item in data['data']:
        formatted_item = {
            'Title': item['title'],
            'Description': item['description'],
            'URL': item['url'],
            'News Site': item['news_site'],
            'Thumbnail': item['thumb_2x']
        }
        formatted_data.append(formatted_item)
    return formatted_data


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

    try:
        # Fetch data from the database
        for trans in session.query(Transaction).all():
            if trans.user_id == user_id:
                coin_name_list.append(trans.coin_name)
                amount_list.append(trans.amount)
                symbol_list.append(trans.symbol)
                price_purchased_at_list.append(trans.price_purchased_at)

                # Make API request to get coin data
                url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
                api_key = "05bf26b5-a99a-4eb7-92f4-e2c8bc263693"
                headers = {'Accepts': 'application/json', 'X-CMC_PRO_API_KEY': api_key}
                params = {'start': '1', 'limit': '5000', 'convert': 'USD'}
                data = requests.get(url, params=params, headers=headers).json()

                # Process coin data
                for i in range(0, 5000):
                    if data['data'][i]['name'].lower() == trans.coin_name.lower():
                        no_of_coins = float(trans.amount) / data['data'][i]['quote']['USD']['price']
                        no_of_coins_list.append(no_of_coins)
                        time_transacted_list.append(trans.time_transacted)
                        time_updated_list.append(trans.time_updated)

        # Calculate portfolio worth
        portfolio_worth = sum(amount_list)

        # Close the session
        session.close()

        # Assign the length of coin_name_list
        length = len(coin_name_list)

        # Create a list of dictionaries containing transaction data
        trans_list = []
        for i in range(length):
            trans_dict = {
                'coin_name': coin_name_list[i],
                'amount': amount_list[i],
                'symbol': symbol_list[i],
                'price_purchased_at': price_purchased_at_list[i],
                'no_of_coins': no_of_coins_list[i],
                'time_transacted': time_transacted_list[i],
                'time_updated': time_updated_list[i]
            }
            trans_list.append(trans_dict)

        # Render the template with the fetched data
        return render_template('transactions.html',
                               user_id=user_id,
                               trans_list=trans_list,
                               portfolio_worth=portfolio_worth,
                               length=length)  # Pass the length variable to the template

    except (RequestException, ConnectionError, Timeout, TooManyRedirects) as e:
        # Handle the specific exception and return an appropriate response
        return f"An error occurred: {str(e)}", 500


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
 

@views.route('/<user_id>/transactions/remove_transaction', methods=['POST'])
def remove_transaction(user_id):
    """Endpoint to update a transaction"""
    coin_name = request.form.get('coin_name')
    coin_name = coin_name.lower()
    amount = request.form.get('amount')
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
                    new_amount = float(trans.amount) - float(amount)
                    trans.amount = new_amount
                    trans.no_of_coins = float(trans.no_of_coins) - (float(amount) / price_purchased_at)
                    trans.time_updated = datetime.now()
                    portfolio_worth = float(session.query(User).get(user_id).portfolio_worth) - new_amount
                    session.query(User).get(user_id).portfolio_worth = portfolio_worth
                    session.commit()
                    session.close()
                    return redirect(url_for("views.transactions", user_id=user_id))
    return "Coin is not present in your portfolio"