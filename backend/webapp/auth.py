from flask import Blueprint, request, flash, make_response, redirect, url_for, jsonify
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


@auth.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return {'message': 'Logout successful'}, 200


@auth.route('/sign-up', methods=['GET', 'POST']) 
def sign_up():
    if request.method == 'POST':
        data = request.json

        email = data.get('email')
        username = data.get('username')
        password1 = data.get('password1')
        password2 = data.get('password2')

        # Validate the input data
        if len(email) < 4:
            return jsonify(message='Email must be greater than 3 characters.'), 400
        elif len(username) < 2:
            return jsonify(message='Username must be greater than 1 character.'), 400
        elif password1 != password2:
            return jsonify(message="Passwords don't match."), 400
        elif len(password1) < 7:
            return jsonify(message='Password must be at least 7 characters.'), 400

        # Check if the username or email already exists
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        for user in session.query(User).all():
            if user.username == username:
                return jsonify(message='This username is already taken, try again with another username!'), 400
        for user in session.query(User).all():
            if user.email == email:
                return jsonify(message='This email already exists, try again with another email!'), 400

        # Create a new user and save it to the database
        new_user = User(username=username, email=email, password=generate_password_hash(password1, method='sha256'))
        session.add(new_user)
        session.commit()
        user_id = new_user.id
        username = new_user.username

        return jsonify(message='Account created successfully. Welcome back {username}!', user_id=user_id), 200

    return jsonify({'message': 'Invalid request'}), 400

@auth.route('/guest')
def guest():
    if not current_user.is_authenticated:
        # Create a guest user
        guest_user = User(username='Guest', email='guest@example.com', password='', access=0)
        login_user(guest_user, remember=True)
        flash('Guest login successful. Welcome!', category='success')
    return redirect(url_for('views.home'))
