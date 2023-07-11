from datetime import datetime, timedelta
from webapp import mail
import json
import os
import requests
from flask import Blueprint, flash, render_template, request, redirect, url_for, abort
from flask_mail import Message
from flask_login import login_required, current_user
from requests.exceptions import RequestException, ConnectionError, Timeout, TooManyRedirects
from werkzeug.security import generate_password_hash, check_password_hash
from .models import *
from .config import *
import cgi

views = Blueprint('views', __name__)

LIVE_PRICE_URL = "https://api.coingecko.com/api/v3/simple/price"

# Send the password reset email


@staticmethod
def send_reset_email(user):
    token = user.generate_reset_token()
    reset_url = url_for('views.reset_password', token=token, _external=True)
    message = f"Click the following link to reset your password: {reset_url}"
    msg = Message('Password Reset',
                  sender=os.environ['MAIL_USERNAME'], recipients=[user.email])
    msg.body = message
    mail.send(msg)
    

@views.route('/', methods=['GET', 'POST'])
def landing():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        # Check if checked checkbox is selected
        send_copy = 'send_copy' in request.form

        recipients = [os.environ['MAIL_USERNAME']]

        if send_copy:
            recipients.append(email)

        msg = Message('New Message from Trackc Contact form',
                      sender=os.environ['MAIL_USERNAME'], recipients=recipients)
        msg.body = f"Name: {name}\nEmail: {email}\nMessage: {message}"

        try:
            mail.send(msg)
            flash('Message sent successfully!', 'success')
        except Exception as e:
            flash(
                'An error occurred while sending the message. Please try again.', 'error')
            print(str(e))
    return render_template('landing.html')


@views.route('/about/<user_id>')
def about(user_id):
    return render_template("about.html", user_id=user_id)


@views.route('/home/<user_id>')
@login_required
def home(user_id):
    """Home Endpoint"""
    # API call to get top 10 cryptocurrencies from CoinGecko
    url = 'https://api.coingecko.com/api/v3/coins/markets'
    parameters = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 10,
        'page': 1
    }    
    response = requests.get(url, params=parameters)
    data = response.json()
    results = data
    for result in results:
        result['current_price'] = '$ ' + "{:,.2f}".format(float(result['current_price']))
        result['total_volume'] = '$ ' + "{:,.2f}".format(result['total_volume'])
        result['price_change_percentage_24h'] = "{:,.2f}".format(float(result['price_change_percentage_24h'])) + '%'

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
    url = "https://api.coingecko.com/api/v3/simple/price"
    headers = {'Accepts': 'application/json'}
    params = {'ids': ','.join(coin_prices.keys()), 'vs_currencies': 'usd'}
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

            if coin_name in data:
                current_price = data[coin_name]['usd']
                current_value = current_price * float(trans.no_of_coins)
                equity = (current_value - (float(trans.no_of_coins)
                          * float(trans.price_purchased_at))) / 100
                current_values[coin_name] = current_value
                equities[coin_name] = equity

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

    # Render results on the homepage
    return render_template("home.html",
                           user_id=user_id,
                           username=user.username.title(),
                           results=results,
                           user=current_user,
                           portfolio_worth=portfolio_worth,
                           portfolio_equity=portfolio_equity)


@views.route('/<user_id>/news', methods=['GET'])
@login_required
def news(user_id):
    # Endpoint to make NewsApi calls
    news_url = "https://api.coingecko.com/api/v3/news"
    formatted_data = get_formatted_news_data(news_url)
    return render_template('news.html', news=formatted_data, user_id=user_id)


def get_formatted_news_data(news_url):
    response = requests.get(news_url)
    data = response.json()
    formatted_data = format_data(data)

    if not formatted_data:
        flash('No news available.', category='info')

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


@views.route('/<user_id>/transactions', methods=['GET', 'POST'])
@login_required
def transactions(user_id):
    if request.method == 'POST':
        portfolio_worth = request.form.get("portfolio_worth")
        user = User.query.get(user_id)
        user.portfolio_worth = float(portfolio_worth)
        user.portfolio_worth_list = user.portfolio_worth_list + [{'x': datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'y':float(portfolio_worth)}]
        db.session.commit()
        portfolio_worth_list = user.portfolio_worth_list
    """Endpoint to fetch data from the database"""

    coin_name_list = []
    amount_spent_list = []
    symbol_list = []
    price_purchased_at_list = []
    no_of_coins_list = []
    time_transacted_list = []
    time_updated_list = []
    image_link_list = []

    # Fetch data from the database
    user = User.query.get(user_id)
    transactions = Transaction.query.filter_by(user_id=user_id).all()

    coin_prices = {}
    for trans in transactions:
        coin_prices[trans.coin_name.lower()] = trans.price_purchased_at

    # Make API request to get live price for the coin
    url = "https://api.coingecko.com/api/v3/coins/markets"
    headers = {'Accepts': 'application/json'}
    params = {'ids': ','.join(coin_prices.keys()), 'vs_currency': 'usd', 'order': ' id_desc'}
    data = requests.get(url, params=params, headers=headers).json()
    #print(data)
    current_values = {}
    equities = {}

    try: 
        for trans in transactions:
            #print(coin_prices.keys())
            coin_name = trans.coin_name.lower()
            print(coin_name)
            coin_name_list.append(trans.coin_name)
            amount_spent_list.append(trans.amount_spent * -1)
            print(trans.amount_spent)
            symbol_list.append(trans.symbol)
            print(trans.symbol)
            price_purchased_at_list.append(trans.price_purchased_at)
            no_of_coins = trans.no_of_coins 
            for i in range(len(data)):
                if data[i]['id'] == coin_name:
                    current_price = data[i]['current_price']
                    current_value = current_price * float(trans.no_of_coins)
                    image_link_list.append(data[i]['image'])
                    break
                elif data[i]['id'] != coin_name and i+1 == len(data):
                    error_message = "An error occurred"
                    flash(error_message, category='error')
                    return redirect(url_for('views.home', user_id=user_id))
            equity = ((float(current_price) - float(trans.price_purchased_at)) / float(trans.price_purchased_at)) * 100
            current_values[coin_name] = current_value
            equities[coin_name] = equity
            no_of_coins_list.append(no_of_coins)
            time_transacted_list.append(trans.time_transacted)
            time_updated_list.append(trans.time_updated)

        # Calculate portfolio worth
        portfolio_worth = sum(current_values.values())
        portfolio_equity = sum(equities.values())

        # Sort transactions by time_updated in descending order (most recent on top)
        sorted_transactions = sorted(
            zip(coin_name_list, amount_spent_list, symbol_list, price_purchased_at_list, no_of_coins_list,
                time_transacted_list, time_updated_list, image_link_list, current_values, equities),
            key=lambda x: x[-2], reverse=True
        )

        # Create a list of dictionaries containing transaction data
        trans_list = []
        for (
            coin_name, amount_spent, symbol, price_purchased_at, no_of_coins, time_transacted,
            time_updated, image_link, current_value, equity
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
                'image_link': image_link,
                'current_value': current_value,
                'equity': equity
            }
            trans_list.append(trans_dict)
        # Close the session
        db.session.close()
        #get portfolio_worth_list from the database
        user = User.query.get(user_id)
        portfolio_worth_list = user.portfolio_worth_list
        #get a list of cryptocurrencies
        try:
            params = {'vs_currency': 'usd', 'per_page': 100, 'page': 1}
            headers = {'Accepts': 'application/json'}
            crypto_list = requests.get('https://api.coingecko.com/api/v3/coins/markets', params=params,headers=headers).json()
            crypto_name_list = []
            for i in range(len(crypto_list)):
                crypto_name_list.append(crypto_list[i]['name'])
        except Exception as e:
            pass
            # error_message = f"An error occurred: {str(e)}"
            # flash(error_message, category='error')

        #Render the template with the fetched data for the user
        return render_template("transactions.html",
                               user_id=user_id,
                               username=user.username.title(),
                               trans_list=trans_list,
                               length=len(trans_list),
                               portfolio_worth=portfolio_worth,
                               portfolio_equity=portfolio_equity,
                               total_amount_spent=sum(amount_spent_list),
                               crypto_name_list=crypto_name_list,
                               portfolio_worth_list=portfolio_worth_list
                               )    
    except Exception as e:
        # Handle the specific exception and flash an appropriate response
        error_message = f"An error occurred."
        flash(error_message, category='error')
        return redirect(url_for('views.home', user_id=user_id))    


@views.route('/<user_id>/transactions/add_transaction', methods=['POST'])
def new_transactions(user_id):
    """Endpoint to add a new transaction"""
    try:
        # Retrieve form data from the frontend
        coin_name = request.form.get('coin_name').strip()
        coin_name = coin_name.lower()
        no_of_coins = request.form.get('no_of_coins')
        price_purchased_at = request.form.get('price_purchased_at')
        amount_spent = float(price_purchased_at) * float(no_of_coins)
        # Check if any of the form data is missing
        if not coin_name or not no_of_coins or not price_purchased_at:
            flash("Please provide all required data.", category="error")
            return redirect(url_for("views.transactions", user_id=user_id))

        # Setup CoinMarketCap API 
        url = "https://api.coingecko.com/api/v3/coins/markets"
        headers = {'Accepts': 'application/json'}
        params = {'ids': coin_name, 'vs_currency': 'usd', 'order': ' id_desc'}
        data = requests.get(url, params=params, headers=headers).json()
        print(data)
        if data is None or data == []:
            flash("Please provide correct data or try again.", category="error")
            return redirect(url_for("views.transactions", user_id=user_id))

        current_price = data[0]['current_price']
        symbol = data[0]['symbol'].upper()

            #return redirect(url_for('views.home', user_id=user_id))
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
            user.portfolio_worth = portfolio_worth
            session.commit()
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
            flash("Transaction added successfully.", category="success")
        
        user = User.query.get(user_id)
        user.portfolio_worth_list = user.portfolio_worth_list + [{'x': datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'y':portfolio_worth}]
        
        new_history = TransactionHistory(
            user_id=user_id,
            coin_name=coin_name,
            symbol=symbol,
            price_purchased_at=price_purchased_at,
            amount_spent=amount_spent,
            no_of_coins=no_of_coins,
            time_transacted=datetime.now(),
            transaction_type = 0
        )
        session.add(new_history)
        session.commit()
        session.close()

        # If no matching cryptocurrency found
        if data is None:
            flash("Unable to add transaction.", category="error")
        return redirect(url_for("views.transactions", user_id=user_id))

    except (RequestException, ConnectionError, Timeout, TooManyRedirects, KeyError) as e:
        # Handle the specific exception and flash an appropriate response
        flash("An error occurred while adding the transaction.", category="error")
        return redirect(url_for("views.transactions", user_id=user_id))


@views.route('/<user_id>/transactions/remove_transaction', methods=['POST'])
@login_required
def remove_transaction(user_id):
    """Endpoint to update a transaction"""
    coin_name = request.form.get('coin_name').strip()
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
                new_amount_spent = float(trans.amount_spent) - (float(price_sold) * float(no_of_coins))
                trans.amount_spent = new_amount_spent
                trans.no_of_coins = new_no_of_coins
                trans.time_updated = datetime.now()
                portfolio_worth = float(User.query.get(user_id).portfolio_worth) - (float(price_sold) * float(no_of_coins))
                User.query.get(user_id).portfolio_worth = portfolio_worth
                User.query.get(user_id).portfolio_worth_list = User.query.get(user_id).portfolio_worth_list + [{'x': datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'y':portfolio_worth}]
                new_history = TransactionHistory(
                        user_id=user_id,
                        coin_name=coin_name,
                        symbol=trans.symbol,
                        price_purchased_at=price_sold,
                        amount_spent=new_amount_spent,
                        no_of_coins=no_of_coins,
                        time_transacted=datetime.now(),
                        transaction_type = 1
                        )
                db.session.add(new_history)
                if new_no_of_coins <= 0:
                    db.session.delete(trans)
                db.session.commit()
                db.session.close()
                flash("Transaction removed successfully.", category="success")
                return redirect(url_for("views.transactions", user_id=user_id))

        # If no matching cryptocurrency found
        flash("Coin is not present in your portfolio", category="error")
        return redirect(url_for("views.transactions", user_id=user_id))

    except (RequestException, ConnectionError, Timeout, TooManyRedirects, KeyError) as e:
        # Handle the specific exception and flash an appropriate response
        flash("An error occurred!", category="error")
        return redirect(url_for("views.transactions", user_id=user_id))
    
@views.route('/<user_id>/transaction-history', methods=['GET'])
@login_required
def transaction_history(user_id):
    """Endpoint to fetch data from the database"""

    coin_name_list = []
    amount_spent_list = []
    symbol_list = []
    price_purchased_at_list = []
    no_of_coins_list = []
    time_transacted_list = []
    #image_link_list = []
    transaction_type_list = []

    # Fetch data from the database
    user = User.query.get(user_id)
    transaction_history = TransactionHistory.query.filter_by(user_id=user_id).all()

    try: 
        for trans in transaction_history:
            #print(coin_prices.keys())
            coin_name = trans.coin_name.capitalize()
            coin_name_list.append(trans.coin_name)
            amount_spent_list.append(trans.amount_spent * -1)
            symbol_list.append(trans.symbol)
            price_purchased_at_list.append(trans.price_purchased_at)
            no_of_coins = trans.no_of_coins 
            no_of_coins_list.append(no_of_coins)
            time_transacted_list.append(trans.time_transacted)
            #image_link_list.append(trans.image_link)
            transaction_type_list.append(trans.transaction_type)

        # Sort transactions by time_updated in descending order (most recent on top)
        sorted_transactions = sorted(
            zip(coin_name_list, amount_spent_list, symbol_list, price_purchased_at_list, no_of_coins_list,
                time_transacted_list, transaction_type_list),
            key=lambda x: x[-2], reverse=True
        )

        # Create a list of dictionaries containing transaction data
        trans_list = []
        for (
            coin_name, amount_spent, symbol, price_purchased_at, no_of_coins, time_transacted,
            transaction_type
        ) in sorted_transactions:
            trans_dict = {
                'coin_name': coin_name,
                'amount_spent': amount_spent,
                'symbol': symbol,
                'price_purchased_at': price_purchased_at,
                'no_of_coins': no_of_coins,
                'transaction_type': transaction_type,
                'time_transacted': time_transacted,
            }
            trans_list.append(trans_dict)
        # Close the session
        db.session.close()
        # Render the template with the fetched data for the user
        return render_template("transaction_history.html",
                               user_id=user_id,
                               username=user.username.title(),
                               trans_list=trans_list
                               )    
    except Exception as e:
        # Handle the specific exception and flash an appropriate response
        flash('An error occurred!', category='error')
        print(e)
        return redirect(url_for('views.transactions', user_id=user_id))


# route for password reset request
@views.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if request.method == 'POST':
        email = request.form['email']
        # Check if the user exists and retrieve their details
        user = User.query.filter_by(email=email).first()

        if user:
            # Send the reset email
            send_reset_email(user)

        flash('An email with instructions to reset your password has been sent.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('reset_password_request.html')

# Route for resetting the password


@views.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    # Check if the token is valid
    if User.verify_reset_token(token) is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('auth.reset_password_request'))
    else:
        if request.method == 'POST':
            password = request.form.get('password')
            verify_password = request.form.get('verify_password')

            if not password or not verify_password or password != verify_password:
                flash('Passwords don\'t match.', category='error')
            elif len(password) < 7:
                flash('Password must be at least 7 characters.', category='error')

            # Update the user's password
            user = User.verify_reset_token(token)
            hashed_new_password = generate_password_hash(
                password, method='sha256')
            user.password = hashed_new_password
            db.session.commit()
            flash(
                'Your password has been successfully reset. Please login with your new password.', 'success')
            return redirect(url_for('auth.login'))
        return render_template('reset_password.html', token=token)

