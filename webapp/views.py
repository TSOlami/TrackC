import datetime
import json
from flask import Blueprint, flash, render_template, request, redirect, url_for, jsonify
from flask_login import login_required, current_user
from sqlalchemy.orm import sessionmaker
import requests
from requests.exceptions import RequestException, ConnectionError, Timeout, TooManyRedirects
from .models import *
import datetime
#from newsapi import NewsApiClient
from newsapi.newsapi_client import NewsApiClient

views = Blueprint('views', __name__)

LIVE_PRICE_URL = "https://api.coingecko.com/api/v3/simple/price"


@views.route ('/')
def landing():
    return render_template("landing.html")


@views.route('/home/<user_id>')
@login_required
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
        'X-CMC_PRO_API_KEY': '032b9c4e-d442-4fdf-8359-ca6736c4216c'
    }
    # Create a session
    session = requests.Session()
    session.headers.update(headers)
    
    response = session.get(url, params=parameters)
    data = json.loads(response.text)
    results = data['data']

    for result in results:
        result['quote']['USD']['price'] = '$ ' + "{:.2f}".format(result['quote']['USD']['price'])
        result['quote']['USD']['volume_24h'] = '$ ' + "{:.2f}".format(result['quote']['USD']['volume_24h'])
        result['quote']['USD']['percent_change_24h'] = "{:.2f}".format(result['quote']['USD']['percent_change_24h']) + '%'

    #Render results on the homepage
    user_id = request.args.get('user_id')
    return render_template("home.html", user_id=user_id, results=results, user=current_user)

@views.route ('/news')
@login_required
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
@login_required
def transactions(user_id):
    """Endpoint to fetch data from the database"""
    user_id = request.args.get('user_id')

    coin_name_list = []
    amount_list = []
    symbol_list = []
    price_purchased_at_list = []
    no_of_coins_list = []
    time_transacted_list = []
    time_updated_list = []
    current_value_list = []
    equity_list = []

    # Fetch data from the database
    transactions = Transaction.query.filter_by(user_id=user_id).all()

    try:
        for trans in transactions:
            
            coin_name_list.append(trans.coin_name)
            amount_list.append(trans.amount)
            symbol_list.append(trans.symbol)
            price_purchased_at_list.append(trans.price_purchased_at)

            # Make API request to get live price for the coin
            params = {
                'ids': trans.coin_name,
                'vs_currencies': 'USD',
            }
            response = requests.get(LIVE_PRICE_URL, params=params)
            if response.status_code == 200:
                data = response.json()
                live_price = data.get(trans.coin_name, {}).get('usd')
                if live_price is not None:
                    current_value = live_price * float(trans.amount)
                    equity = current_value - (float(trans.amount) * float(trans.price_purchased_at))
                    current_value_list.append(current_value)
                    equity_list.append(equity)

            no_of_coins = float(trans.amount) / float(trans.price_purchased_at)
            no_of_coins_list.append(no_of_coins)
            time_transacted_list.append(trans.time_transacted)
            time_updated_list.append(trans.time_updated)

        # Calculate portfolio worth
        portfolio_worth = sum(current_value_list)

        

        # Calculate portfolio equity 
        portfolio_equity = sum(equity_list)
        
        # Sort transactions by time_updated in descending order (most recent on top)
        sorted_transactions = sorted(
            zip(coin_name_list, amount_list, symbol_list, price_purchased_at_list, no_of_coins_list,
                time_transacted_list, time_updated_list, current_value_list, equity_list),
            key=lambda x: x[-2], reverse=True
        )
        # Assign the length of coin_name_list
        length = len(coin_name_list)

        # Create a list of dictionaries containing transaction data
        trans_list = []
        for (
            coin_name, amount, symbol, price_purchased_at, no_of_coins, time_transacted,
            time_updated, current_value, equity
        ) in sorted_transactions:
            trans_dict = {
                'coin_name': coin_name,
                'amount': amount,
                'symbol': symbol,
                'price_purchased_at': price_purchased_at,
                'no_of_coins': no_of_coins,
                'time_transacted': time_transacted,
                'time_updated': time_updated,
                'current_value': current_value,
                'equity': equity
            }
            trans_list.append(trans_dict)
        # Close the session
        db.session.close()
        
        # Render the template with the fetched data for the user
        user_id = request.args.get('user_id')
        return render_template(
            'transactions.html',
            user_id=user_id,
            trans_list=trans_list,
            length=len(coin_name_list),
            portfolio_worth=portfolio_worth
        )
    
    except (RequestException, ConnectionError, Timeout, TooManyRedirects) as e:
        # Handle the specific exception and flash an appropriate response
        flash('An error occurred!', category='error')
        


@views.route('/<user_id>/transactions/add_transaction', methods=['POST'])
@login_required
def new_transactions(user_id):
    """Endpoint to add a new transaction"""
    try:
        # Retrieve form data from the frontend
        coin_name = request.form.get('coin_name')
        coin_name = coin_name.lower()
        amount = request.form.get('amount')

        # Setup CoinMarketCap API 
        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
        api_key = "032b9c4e-d442-4fdf-8359-ca6736c4216c"
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
                session = db.session()

                # Check if the transaction already exists for the user and coin
                existing_trans = Transaction.query.filter_by(coin_name=coin_name, user_id=user_id).first()
                if existing_trans:
                    # Update the existing transaction
                    existing_trans.amount = float(amount) + float(existing_trans.amount)
                    existing_trans.no_of_coins = float(existing_trans.no_of_coins) + (float(amount) / price_purchased_at)
                    existing_trans.time_updated = datetime.datetime.now()
                    user = User.query.get(user_id)
                    user.portfolio_worth = float(user.portfolio_worth) + float(amount)
                    session.commit()
                else:
                    # Create a new transaction
                    user = User.query.get(user_id)
                    portfolio_worth = float(user.portfolio_worth) + float(amount)
                    new_trans = Transaction(
                        user_id=user_id,
                        amount=amount,
                        coin_name=coin_name.capitalize(),
                        symbol=symbol,
                        price_purchased_at=price_purchased_at,
                        no_of_coins=no_of_coins
                    )
                    session.add(new_trans)
                    user.portfolio_worth = portfolio_worth
                    session.commit()

                # Close the session
                session.close()

                return redirect(url_for("views.transactions", user_id=user_id))

        # If no matching cryptocurrency found
        flash("Unable to add transaction.", category="error")
        return redirect(url_for("views.transactions", user_id=user_id))

    except (RequestException, ConnectionError, Timeout, TooManyRedirects) as e:
        # Handle the specific exception and flash an appropriate response
        flash("An error occurred while adding the transaction.", category="error")
        return redirect(url_for("views.transactions", user_id=user_id))
    

@views.route('/<user_id>/transactions/remove_transaction', methods=['POST'])
@login_required
def remove_transaction(user_id):
    """Endpoint to update a transaction"""
    coin_name = request.form.get('coin_name')
    coin_name = coin_name.lower()
    amount = request.form.get('amount')

    try:
        transactions = Transaction.query.filter_by(user_id=user_id).all()

        for trans in transactions:
            if trans.coin_name.lower() == coin_name:
                url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
                api_key = "05bf26b5-a99a-4eb7-92f4-e2c8bc263693"
                headers = {'Accepts': 'application/json', 'X-CMC_PRO_API_KEY': api_key}
                params = {'start': '1', 'limit': '5000', 'convert': 'USD'}
                data = requests.get(url, params=params, headers=headers).json()

                for i in range(0, 5000):
                    if data['data'][i]['name'].lower() == coin_name:
                        price_purchased_at = data['data'][i]['quote']['USD']['price']
                        new_amount = float(trans.amount) - float(amount)
                        trans.amount = new_amount
                        trans.no_of_coins = float(trans.no_of_coins) - (float(amount) / price_purchased_at)
                        trans.time_updated = datetime.now()
                        portfolio_worth = float(User.query.get(user_id).portfolio_worth) - new_amount
                        User.query.get(user_id).portfolio_worth = portfolio_worth
                        db.session.commit()
                        db.session.close()
                        return redirect(url_for("views.transactions", user_id=user_id))

        # If no matching cryptocurrency found
        flash("Coin is not present in your portfolio", category="error")
        return redirect(url_for("views.transactions", user_id=user_id))

    except (RequestException, ConnectionError, Timeout, TooManyRedirects) as e:
        # Handle the specific exception and flash an appropriate response
        flash("An error occurred!", category="error")
        return redirect(url_for("views.transactions", user_id=user_id))
