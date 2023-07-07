import datetime
import json
from flask import Blueprint, flash, render_template, request, redirect, url_for
from flask_login import login_required, current_user
import requests
from requests.exceptions import RequestException, ConnectionError, Timeout, TooManyRedirects
from .models import *
from datetime import datetime

views = Blueprint('views', __name__)

LIVE_PRICE_URL = "https://api.coingecko.com/api/v3/simple/price"


@views.route ('/')
def landing():
    return render_template("landing.html")


@views.route('/about')
def about():
    return render_template("about.html")


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
        result['quote']['USD']['price'] = '$ ' + "{:,.2f}".format(result['quote']['USD']['price'])
        result['quote']['USD']['volume_24h'] = '$ ' + "{:,.2f}".format(result['quote']['USD']['volume_24h'])
        result['quote']['USD']['percent_change_24h'] = "{:,.2f}".format(result['quote']['USD']['percent_change_24h']) + '%'
    
    coin_name_list = []
    amount_spent_list = []
    symbol_list = []
    price_purchased_at_list = []
    no_of_coins_list = []
    time_transacted_list = []
    time_updated_list = []

    # Fetch data from the database
    user = User.query.get(user_id)
    transactions = Transaction.query.filter_by(user_id=user_id).all()

    coin_prices = {}
    for trans in transactions:
        coin_prices[trans.coin_name.lower()] = trans.price_purchased_at

    
    # Make API request to get live price for the coin
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    api_key = "05bf26b5-a99a-4eb7-92f4-e2c8bc263693"
    headers = {'Accepts': 'application/json', 'X-CMC_PRO_API_KEY': api_key}
    params = {'start': '1', 'limit': '5000', 'convert': 'USD'}
    data = requests.get(url, params=params, headers=headers).json()

    current_values = {}
    equities = {}

    try:
        for trans in transactions:
            coin_name = trans.coin_name.lower()
            coin_name_list.append(trans.coin_name)
            amount_spent_list.append(trans.amount_spent)
            symbol_list.append(trans.symbol)
            price_purchased_at_list.append(trans.price_purchased_at)
            no_of_coins = trans.no_of_coins

            for i in range(0, 5000):
                if data['data'][i]['name'].lower() == trans.coin_name.lower(): 
                    current_price = data['data'][i]['quote']['USD']['price']
                    current_value = current_price * float(trans.no_of_coins)
                    equity = (current_value - (float(trans.no_of_coins) * float(trans.price_purchased_at))) / 100
                    current_values[coin_name] = current_value
                    equities[coin_name] = equity
                    break
            no_of_coins_list.append(no_of_coins)
            time_transacted_list.append(trans.time_transacted)
            time_updated_list.append(trans.time_updated)

        # Calculate portfolio worth
        portfolio_worth = sum(current_values.values())
        portfolio_equity = sum(equities.values())
        
    except Exception as e:
        # Handle the specific exception and flash an appropriate response
        print(f"Error occurred: {str(e)}")
        flash('An error occurred!', category='error')

    #Render results on the homepage
    return render_template("home.html", 
                           user_id=user_id, 
                           username=user.username.title(),
                           results=results,
                           user=current_user,
                           portfolio_worth=portfolio_worth,
                           portfolio_equity=portfolio_equity)

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

    coin_name_list = []
    amount_spent_list = []
    symbol_list = []
    price_purchased_at_list = []
    no_of_coins_list = []
    time_transacted_list = []
    time_updated_list = []

    # Fetch data from the database
    user = User.query.get(user_id)
    transactions = Transaction.query.filter_by(user_id=user_id).all()
    
    coin_prices = {}
    for trans in transactions:
        coin_prices[trans.coin_name.lower()] = trans.price_purchased_at


    # Make API request to get live price for the coin
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    api_key = "05bf26b5-a99a-4eb7-92f4-e2c8bc263693"
    headers = {'Accepts': 'application/json', 'X-CMC_PRO_API_KEY': api_key}
    params = {'start': '1', 'limit': '5000', 'convert': 'USD'}
    data = requests.get(url, params=params, headers=headers).json()

    current_values = {}
    equities = {}

    try:
        for trans in transactions:
            coin_name = trans.coin_name.lower()
            coin_name_list.append(trans.coin_name)
            amount_spent_list.append(trans.amount_spent)
            symbol_list.append(trans.symbol)
            price_purchased_at_list.append(trans.price_purchased_at)
            no_of_coins = trans.no_of_coins 

            
            for i in range(0, 5000):
                if data['data'][i]['name'].lower() == trans.coin_name.lower(): 
                    current_price = data['data'][i]['quote']['USD']['price']
                    current_value = current_price * float(trans.no_of_coins)
                    equity = (current_value - (float(trans.no_of_coins) * float(trans.price_purchased_at))) / 100
                    current_values[coin_name] = current_value
                    equities[coin_name] = equity
                    break
            no_of_coins_list.append(no_of_coins)
            time_transacted_list.append(trans.time_transacted)
            time_updated_list.append(trans.time_updated)


        # Calculate portfolio worth
        portfolio_worth = sum(current_values.values())
        portfolio_equity = sum(equities.values())
        
        # Sort transactions by time_updated in descending order (most recent on top)
        sorted_transactions = sorted(
            zip(coin_name_list, amount_spent_list, symbol_list, price_purchased_at_list, no_of_coins_list,
                time_transacted_list, time_updated_list, current_values, equities),
            key=lambda x: x[-2], reverse=True
        )

        # Create a list of dictionaries containing transaction data
        trans_list = []
        
        for (
            coin_name, amount_spent, symbol, price_purchased_at, no_of_coins, time_transacted,
            time_updated, current_value, equity
        ) in sorted_transactions:
            current_value = current_values[coin_name.lower()]  
            equity = equities[coin_name.lower()]
            trans_dict = {
                'coin_name': coin_name,
                'amount_spent': amount_spent,
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
        return render_template(
            'transactions.html',
            user_id=user_id,
            username=user.username.title(),
            trans_list=trans_list,
            length=len(trans_list),
            portfolio_worth=portfolio_worth,
            portfolio_equity=portfolio_equity)
    
    except Exception as e:
        # Handle the specific exception and flash an appropriate response
        print(f"Error occurred: {str(e)}")
        flash('An error occurred!', category='error')
        return redirect(url_for('views.transactions', user_id=user_id))
        


@views.route('/<user_id>/transactions/add_transaction', methods=['POST'])
def new_transactions(user_id):
    """Endpoint to add a new transaction"""
    try:
        # Retrieve form data from the frontend
        coin_name = request.form.get('coin_name')
        coin_name = coin_name.lower()
        no_of_coins = request.form.get('no_of_coins')        
        price_purchased_at = request.form.get('price_purchased_at')
        amount_spent = float(price_purchased_at) * float(no_of_coins)

        # Check if any of the form data is missing
        if not coin_name or not no_of_coins or not price_purchased_at:
            flash("Please provide all required data.", category="error")
            return redirect(url_for("views.transactions", user_id=user_id))

        # Setup CoinMarketCap API 
        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
        api_key = "032b9c4e-d442-4fdf-8359-ca6736c4216c"
        headers = {'Accepts': 'application/json', 'X-CMC_PRO_API_KEY': api_key}
        params = {'start': '1', 'limit': '5000', 'convert': 'USD'}
        data = requests.get(url, params=params, headers=headers).json()
        print (data)

        # Find the cryptocurrency matching the provided name
        for i in range(0, 5000):
            if data['data'][i]['name'].lower() == coin_name:
                print (data)
                current_price = data['data'][i]['quote']['USD']['price']
                symbol = data['data'][i]['symbol']

                # Create a database session
                session = db.session()

                # Check if the transaction already exists for the user and coin
                existing_trans = Transaction.query.filter_by(user_id=user_id, coin_name=coin_name.capitalize()).first()
                if existing_trans:
                    # Update the existing transaction
                    existing_trans.amount_spent = float(existing_trans.amount_spent) + float(amount_spent)
                    existing_trans.no_of_coins = float(existing_trans.no_of_coins) + float(no_of_coins)
                    existing_trans.time_updated = datetime.now()
                    user = User.query.get(user_id)
                    portfolio_worth = float(user.portfolio_worth) + (float(current_price) * float(no_of_coins))
                    session.commit()
                    session.close()
                    flash("Transaction added successfully.", category="success")
                else:
                    # Create a new transaction
                    user = User.query.get(user_id)
                    portfolio_worth = float(user.portfolio_worth) + (float(current_price) * float(no_of_coins))
                    new_trans = Transaction(
                        user_id=user_id,
                        amount_spent=amount_spent,
                        coin_name=coin_name.capitalize(),
                        symbol=symbol,
                        price_purchased_at=price_purchased_at,
                        no_of_coins=no_of_coins
                    )
                    session.add(new_trans)
                    user.portfolio_worth = portfolio_worth
                    session.commit()
                    session.close()
                    flash("Transaction added successfully.", category="success")
                break

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
    no_of_coins = request.form.get('no_of_coins')
    price_sold = request.form.get('price_sold')

    if not coin_name or not no_of_coins or not price_sold:
        flash("Please provide all required data.", category="error")
        return redirect(url_for("views.transactions", user_id=user_id))
    
    try:
        transactions = Transaction.query.filter_by(user_id=user_id).all()

        for trans in transactions:
            if trans.coin_name.lower() == coin_name:
                new_no_of_coins = float(trans.no_of_coins) - float(no_of_coins)
                new_amount_spent = float(trans.amount_spent) - float(price_sold)
                trans.amount_spent = new_amount_spent
                trans.no_of_coins = new_no_of_coins
                trans.time_updated = datetime.now()
                portfolio_worth = float(User.query.get(user_id).portfolio_worth) - float(price_sold)
                User.query.get(user_id).portfolio_worth = portfolio_worth
                db.session.commit()
                db.session.close()
                flash("Transaction removed successfully.", category="success")
                return redirect(url_for("views.transactions", user_id=user_id))

        # If no matching cryptocurrency found
        flash("Coin is not present in your portfolio", category="error")
        return redirect(url_for("views.transactions", user_id=user_id))

    except (RequestException, ConnectionError, Timeout, TooManyRedirects) as e:
        # Handle the specific exception and flash an appropriate response
        flash("An error occurred!", category="error")
        return redirect(url_for("views.transactions", user_id=user_id))