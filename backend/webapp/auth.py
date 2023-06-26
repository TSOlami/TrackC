from flask import Blueprint, render_template, request, flash, make_response, redirect, url_for, jsonify
from .models import *
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import sessionmaker
from flask_login import login_user,login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST']) 
def login():
    email = request.json.get('email')
    password = request.json.get('password')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    for user in session.query(User).all():
        if (
            user.email == email
            and check_password_hash(user.password, password)
            and (user.access is None or user.access == 1)
        ):
            # Login Successful
            response = {
                'message': f'Login successful. Welcome back {user.username}!',
                'user_id': user.id,
                'status_code': 200
            }
            return jsonify(response), 200
    response = {
        'message': 'Incorrect email address or password. Try again!',
        'status_code': 401
    }
    return jsonify(response), 401


@auth.route('/logout')
@login_required
def logout():
    return redirect(url_for('views.landing'))

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
                flash('This username is already taken, try again with another username!', category='error')
                exc = True
        for user in session.query(User).all():
            if user.email == email:
                flash('This email already exists, try again with another email!', category='error')
                exc = True
                break

        if exc == False:
            new_user = User(username=username, email=email, password=generate_password_hash(password1, method='sha256'))
            session.add(new_user)
            session.commit()
            #flash('Account created successfully, Welcome {}!'.format(user.username), category='success')
            #user_id =  session.query(User).id.order_by(User.date_created.desc())
            for user in session.query(User).all():
                if user.username == username:
                   user_id = user.id
            return redirect(url_for('views.home', user_id=user_id))
    return render_template("sign_up.html", user=current_user)

@auth.route('/guest')
def guest():
    if not current_user.is_authenticated:
        # Create a guest user
        guest_user = User(username='Guest', email='guest@example.com', password='', access=0)
        login_user(guest_user, remember=True)
        flash('Guest login successful. Welcome!', category='success')
    return redirect(url_for('views.home'))
