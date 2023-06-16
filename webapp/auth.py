from flask import Blueprint, render_template, request, flash
from .models import *
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST']) 
def login():
    return render_template("login.html")

@auth.route('/logout')
def logout():
    return "Logout"

@auth.route('/sign-up', methods=['GET', 'POST']) 
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(username) < 2:
            flash('Username must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        
            user_object = User.query.filter_by(username=username).first
            if user_object:
                flash('This username is already taken!', category='error')
            else:
                # Create new user
                new_user = User(username=username, email=email, password=generate_password_hash(password1, method='sha256'))
                db.session.add(new_user)
                db.session.commit()
                flash('Account created!', category='success')
                return "User added to db"

    return render_template("sign_up.html")

@auth.route('/guest')
def guest():
    return render_template("home.html")