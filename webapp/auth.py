from flask import Blueprint,  render_template, request, flash, make_response, redirect, url_for
from .models import *
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user,login_required, logout_user, current_user
from sqlalchemy.exc import IntegrityError

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST']) 
def login():
    """Endpoint to handle User login"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first() 

        if user is not None and check_password_hash(user.password, password) and (user.access is None or user.access == 1):
            # Login Successful
            flash('Login successful. Welcome back {}!'.format(user.username), category='success')
            login_user(user, remember=True)
            user_id = user.id
            return redirect(url_for('views.home', user_id=user_id))
        else:
            # Incorrect email or password
            flash('Incorrect email address or password.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/sign-up', methods=['GET', 'POST']) 
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # Validate the input data
        if not email or len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
            return render_template("sign_up.html")
        elif not username or len(username) < 2:
            flash('Username must be greater than 1 character.', category='error')
            return render_template("sign_up.html")
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
            return render_template("sign_up.html")
        elif not password1 or not password2 or password1 != password2:
            flash('Passwords don\'t match.', category='error')
            return render_template("sign_up.html")

        # Check if the username or email already exists
        
        try:
            user = User.query.filter_by(email=email).first()
            if user:
                #raise IntegrityError('This email is already taken, try again with another email!')
                flash('This email is already taken, try again with another email!', category='error')
                return render_template("sign_up.html")
            
            user = User.query.filter_by(username=username).first()
            if user:
                #raise IntegrityError('This username is already taken, try again with another username!')
                flash('This username is already taken, try again with another username!', category='error')
                return render_template("sign_up.html")


            # Create a new user and save it to the database
            new_user = User(username=username, email=email, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created successfully, Welcome {}!'.format(new_user.username), category='success')
            user_id = new_user.id
            username = new_user.username
            email = new_user.email

            # Close db
            db.session.close()

            return redirect(url_for('views.home', user_id=user_id))
        except IntegrityError as e:
            db.session.rollback()
            flash("An error occurred, please try again or contact our customer support.", category='error')
        except Exception as e:
            db.session.rollback()
            error_message = f"An error occurred: {str(e)}"
            flash(error_message, category='error')
            # Log the error for debugging purposes
            print('Error:', str(e))

    return render_template("sign_up.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))