from datetime import datetime
from webapp import mail
import os
import requests
from flask import Blueprint, flash, render_template, request, redirect, url_for, abort
from flask_mail import Message
from flask_login import login_required, current_user
from requests.exceptions import RequestException, ConnectionError, Timeout, TooManyRedirects, HTTPError
from werkzeug.security import generate_password_hash, check_password_hash
from .models import *
from .config import *

views = Blueprint('views', __name__)

LIVE_PRICE_URL = "https://api.coingecko.com/api/v3/simple/price"

# Send the password reset email
def send_reset_email(user):
    """Send a password reset email to the user"""
    token = user.generate_reset_token()
    reset_url = url_for('views.reset_password', token=token, _external=True)
    message = f"Click the following link to reset your password: {reset_url}"
    msg = Message('Password Reset',
                  sender=os.environ['MAIL_USERNAME'], recipients=[user.email])
    msg.body = message
    mail.send(msg)


@views.route('/', methods=['GET', 'POST'])
def landing():
    """The landing page endpoint"""
    if request.method == 'POST':
        # Collect the form data
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        # Check if checked checkbox is selected
        send_copy = 'send_copy' in request.form

        recipients = [os.environ['MAIL_USERNAME']]

        # Check if the send copy option is selected and send a copy to the user
        if send_copy:
            recipients.append(email)

        msg = Message('New Message from Trackc Contact form',
                      sender=os.environ['MAIL_USERNAME'], recipients=recipients)
        msg.body = f"Name: {name}\nEmail: {email}\nMessage: {message}"
        # Send the message
        try:
            mail.send(msg)
            flash('Message sent successfully!', 'success')
        except Exception as e:
            flash(
                'An error occurred while sending the message. Please try again.', 'error')
    return render_template('landing.html')


@views.route('/about')
def about():
    """The about page endpoint"""
    return render_template("about.html")


@views.route('/home/<user_id>')
@login_required
def home(user_id):
    try:
        # API call to get top 10 cryptocurrencies from CoinGecko
        url = 'https://api.coingecko.com/api/v3/coins/markets'
        parameters = {
            'vs_currency': 'usd',
            'order': 'market_cap_desc',
            'per_page': 10,
            'page': 1
        }    
        response = requests.get(url, params=parameters)
        response.raise_for_status()  # Raise an exception if the response is not successful
        data = response.json()
        results = data
        print(data)
        
        # Iterate through the results and get the required data
        for result in results:
            result['current_price'] = '$ ' + "{:,.2f}".format(float(result['current_price']))
            result['total_volume'] = '$ ' + "{:,.2f}".format(result['total_volume'])
            result['price_change_percentage_24h'] = "{:,.2f}".format(float(result['price_change_percentage_24h'])) + '%'

        # Create a list for storing values
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

        # Create a dictionary for storing values
        coin_prices = {}
        for trans in transactions:
            coin_prices[trans.coin_name.lower()] = trans.price_purchased_at

        # Make API request to get live price for the coin
        url = "https://api.coingecko.com/api/v3/simple/price"
        headers = {'Accepts': 'application/json'}
        params = {'ids': ','.join(coin_prices.keys()), 'vs_currencies': 'usd'}
        data = requests.get(url, params=params, headers=headers).json()

        # Create a dictionary for storing values
        current_values = {}
        equities = {}

        # Get the user data from the db
        try:
            for trans in transactions:
                coin_name = trans.coin_name.lower()
                coin_name_list.append(trans.coin_name)
                amount_spent_list.append(trans.amount_spent)
                symbol_list.append(trans.symbol)
                price_purchased_at_list.append(trans.price_purchased_at)
                no_of_coins = trans.no_of_coins

                # Get the current value for the coins from the api response
                if coin_name in data:
                    current_price = data[coin_name]['usd']
                    current_value = current_price * float(trans.no_of_coins)
                    equity = (current_value - (float(trans.no_of_coins)
                            * float(trans.price_purchased_at))) / 100
                    current_values[coin_name] = current_value
                    equities[coin_name] = equity

                # Save the data into the corresponding list
                no_of_coins_list.append(no_of_coins)
                time_transacted_list.append(trans.time_transacted)
                time_updated_list.append(trans.time_updated)

            # Calculate portfolio worth
            portfolio_worth = sum(current_values.values())
            portfolio_equity = sum(equities.values())

        except requests.exceptions.RequestException:
            # Handle request-related exceptions (e.g., network error)
            flash('An error occurred while fetching data. Please wait for a minute and try again.', category='error')
            return redirect(url_for("views.error_404", user_id=user_id))

        except ValueError:
            # Handle JSON decoding error
            flash('An error occurred while processing data. Please wait for a minute and try again.', category='error')
            return redirect(url_for("views.error_404", user_id=user_id))

        except Exception as e:
            # Handle the specific exception and flash an appropriate response
            flash('An error occurred!', category='error')
            return redirect(url_for("views.error_404", user_id=user_id))

        # Render results on the homepage
        return render_template("home.html",
                            user_id=user_id,
                            username=user.username.title(),
                            results=results,
                            user=current_user,
                            portfolio_worth=portfolio_worth,
                            portfolio_equity=portfolio_equity)
    except requests.exceptions.HTTPError as err:
        # Handle the HTTPError exception and flash an appropriate response
        if err.response.status_code == 429:
            flash('CoinGecko API is temporarily unavailable. Please wait a minute before refreshing the page.', category='error')
        else:
            flash('An unexpected error occurred!', category='error')

    return redirect(url_for('views.error_404', user_id=user_id))
    

@views.route('/<user_id>/news', methods=['GET'])
@login_required
def news(user_id):
    """The news page endpoint"""
    news_url = "https://api.coingecko.com/api/v3/news"
    formatted_data = get_formatted_news_data(news_url)
    return render_template('news.html', news=formatted_data, user_id=user_id)


def get_formatted_news_data(news_url):
    # Returns the news results in json format
    response = requests.get(news_url)
    data = response.json()
    formatted_data = format_data(data)
    # Check if the formatted news is present
    if not formatted_data:
        flash('No news available.', category='info')
    return formatted_data


def format_data(data):
    """Format the news data"""
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
    """The transactions page endpoint"""
    if request.method == 'POST':
        portfolio_worth = request.form.get("portfolio_worth")
        user = User.query.get(user_id)
        user.portfolio_worth = float(portfolio_worth)
        user.portfolio_worth_list = user.portfolio_worth_list + [{'x': datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'y':float(portfolio_worth)}]
        db.session.commit()
        portfolio_worth_list = user.portfolio_worth_list
        
    # Fetch data from the database
    coin_name_list = []
    amount_spent_list = []
    symbol_list = []
    price_purchased_at_list = []
    no_of_coins_list = []
    time_transacted_list = []
    time_updated_list = []
    image_link_list = []

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
    
    current_values = {}
    equities = {}

    try: 
        for trans in transactions:
            coin_name = trans.coin_name.lower()
            coin_name_list.append(trans.coin_name)  # Store the coin name in a list
            amount_spent_list.append(trans.amount_spent * -1)  # Store the negative amount spent (indicating a purchase)
            symbol_list.append(trans.symbol)   # Store the symbol of the coin
            price_purchased_at_list.append(trans.price_purchased_at)  # Store the price at which the coin was purchased
            no_of_coins = trans.no_of_coins  # Get the number of coins

            # Find the matching coin data in the API response
            for i in range(len(data)):
                if data[i]['id'] == coin_name:
                    current_price = data[i]['current_price']  # Get the current price of the coin
                    current_value = current_price * float(trans.no_of_coins)  # Calculate the current value of the coins
                    image_link_list.append(data[i]['image'])  # Store the image link for the coin
                    break
                elif data[i]['id'] != coin_name and i+1 == len(data):
                    # Handle the case when the coin data is not found in the API response
                    error_message = "An error occurred"
                    flash(error_message, category='error')
                    return redirect(url_for('views.home', user_id=user_id))
            equity = ((float(current_price) - float(trans.price_purchased_at)) / float(trans.price_purchased_at)) * 100  # Calculate the equity percentage
            current_values[coin_name] = current_value  # Store the current value for the coin
            equities[coin_name] = equity  # Store the equity percentage for the coin
            no_of_coins_list.append(no_of_coins)  # Store the number of coins
            time_transacted_list.append(trans.time_transacted)  # Store the time of transaction
            time_updated_list.append(trans.time_updated)  # Store the time of last update

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
        # Get portfolio_worth_list from the database
        user = User.query.get(user_id)
        portfolio_worth_list = user.portfolio_worth_list
        # Get a list of cryptocurrencies
        try:
            params = {'vs_currency': 'usd', 'per_page': 100, 'page': 1}
            headers = {'Accepts': 'application/json'}
            crypto_list = requests.get('https://api.coingecko.com/api/v3/coins/markets', params=params,headers=headers).json()
            crypto_name_list = []
            for i in range(len(crypto_list)):
                crypto_name_list.append(crypto_list[i]['name'])
        except Exception as e:
            # Handle the specific exception and flash an appropriate response
            flash("An unexpected error occurred, please wait a minute before trying again", category="error")
            
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
        flash("An unexpected error occurred.", category="error")
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
        if data is None or data == []:
            flash("Please provide correct data or try again.", category="error")
            return redirect(url_for("views.transactions", user_id=user_id))
        
        # Get the required data from the api response
        current_price = data[0]['current_price']
        symbol = data[0]['symbol'].upper()

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
            # Flash a successs message
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
        # Get user data from the database
        user = User.query.get(user_id)
        user.portfolio_worth_list = user.portfolio_worth_list + [{'x': datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'y':portfolio_worth}]
        # Update the existing transaction history
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
    """Endpoint to remove a transaction"""
    coin_name = request.form.get('coin_name').strip()
    coin_name = coin_name.lower()
    no_of_coins = request.form.get('no_of_coins')
    price_sold = request.form.get('price_sold')

    # Check if any of the form data is missing
    if not coin_name or not no_of_coins or not price_sold:
        flash("Please provide all required data.", category="error")
        return redirect(url_for("views.transactions", user_id=user_id))

    try:
        # Fetch user transactions from the database
        transactions = Transaction.query.filter_by(user_id=user_id).all()
        for trans in transactions:
            if trans.coin_name.lower() == coin_name:
                new_no_of_coins = float(trans.no_of_coins) - float(no_of_coins)
                new_amount_spent = float(trans.amount_spent) - (float(price_sold) * float(no_of_coins))
                trans.amount_spent = new_amount_spent
                trans.no_of_coins = new_no_of_coins
                trans.time_updated = datetime.now()
                
                # Perform the specific logic 
                portfolio_worth = float(User.query.get(user_id).portfolio_worth) - (float(price_sold) * float(no_of_coins))
                User.query.get(user_id).portfolio_worth = portfolio_worth
                User.query.get(user_id).portfolio_worth_list = User.query.get(user_id).portfolio_worth_list + [{'x': datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'y':portfolio_worth}]
                
                # Update the existing transaction history
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
                # Update the database
                db.session.add(new_history)
                if new_no_of_coins <= 0:
                    db.session.delete(trans)
                db.session.commit()
                db.session.close()
                
                # Flash a success message
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

    # Fetch the user data from the database
    user = User.query.get(user_id)
    transaction_history = TransactionHistory.query.filter_by(user_id=user_id).all()

    try: 
        for trans in transaction_history:
            coin_name = trans.coin_name.capitalize()  # Capitalize the coin name
            coin_name_list.append(trans.coin_name)  # Store the coin name in a list
            amount_spent_list.append(trans.amount_spent * -1)  # Store the negative amount spent (indicating a purchase)
            symbol_list.append(trans.symbol)  # Store the symbol of the coin
            price_purchased_at_list.append(trans.price_purchased_at)  # Store the price at which the coin was purchased
            no_of_coins = trans.no_of_coins  # Get the number of coins
            no_of_coins_list.append(no_of_coins)  # Store the number of coins
            time_transacted_list.append(trans.time_transacted)  # Store the time of transaction
            transaction_type_list.append(trans.transaction_type)  # Store the transaction type

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


@views.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    """Route for password reset request"""
    if request.method == 'POST':
        # Collect the data from the form
        email = request.form['email']
        # Check if the user exists and retrieve their details
        user = User.query.filter_by(email=email).first()

        if user:
            # Send the reset email
            send_reset_email(user)
        
        # Flash an appropriate response
        flash('An email with instructions to reset your password has been sent.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('reset_password_request.html')


@views.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Endpoint for resetting a user password"""

    # Check if the token is valid and flash a message
    if User.verify_reset_token(token) is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('auth.reset_password_request'))
    else:
        if request.method == 'POST':
            # Collect the data from the form
            password = request.form.get('password')
            verify_password = request.form.get('verify_password')

            # Validate the input
            if not password or not verify_password or password != verify_password:
                flash('Passwords don\'t match.', category='error')
            elif len(password) < 7:
                flash('Password must be at least 7 characters.', category='error')

            # Update the user's password and save it 
            user = User.verify_reset_token(token)
            hashed_new_password = generate_password_hash(
                password, method='sha256')
            user.password = hashed_new_password
            db.session.commit()
            # Flash an appropriate response
            flash(
                'Your password has been successfully reset. Please login with your new password.', 'success')
            return redirect(url_for('auth.login'))
        return render_template('reset_password.html', token=token)


@views.route('/404/<user_id>')
def error_404(user_id):
    # Define the 404 route
    return render_template("error.html", user_id=user_id)


@views.errorhandler(404)
def not_found_error(error):
    # Define the global 404 error handler
    return render_template('error.html'), 404
