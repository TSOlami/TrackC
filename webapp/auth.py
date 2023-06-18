from flask import Blueprint, render_template, request, flash, make_response
from .models import *
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import sessionmaker
import requests

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST']) 
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        for user in session.query(User).all():
            if user.email == email and check_password_hash(user.password, password):
                return render_template("home.html")
        flash('Incorrect email address or password.', category='error')
        
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
        
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        exc = False
        for user in session.query(User).all():
            if user.username == username:
                flash('This username is already taken!', category='error')
                exc = True
        for user in session.query(User).all():
            if user.email == email:
                flash('This email exists!', category='error')
                exc = True

        if exc == False:
            new_user = User(username=username, email=email, password=generate_password_hash(password1, method='sha256'))
            session.add(new_user)
            session.commit()
            flash('Account created!', category='success')
            #response = make_response(login())
            #response.method = 'POST'
            #return response

    return render_template("sign_up.html")

@auth.route('/guest')
def guest():
    return render_template("home.html")
