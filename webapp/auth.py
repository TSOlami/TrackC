from flask import Blueprint, request, jsonify, session
from .models import *
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import sessionmaker
from flask_cors import CORS, cross_origin


auth = Blueprint('auth', __name__)
CORS(auth)


@cross_origin()
@auth.route('/login', methods=['POST']) 
def login():
    data = request.json

    email = data.get('email')
    password = data.get('password')
    
    user = User.query.filter_by(email=email).first() 

    if user is not None and check_password_hash(user.password, password) and (user.access is None or user.access == 1):
        # Login Successful
        response = {
            'message': f'Login successful. Welcome back {user.username}!',
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'status_code': 200
        }

        session["user_id"] = user.id
        return jsonify(response), 200
    else:
        # Incorrect email or password
        response = {
            'message': 'Incorrect email address or password. Try again!',
            'status_code': 401
        }
        return jsonify(response), 401


@cross_origin()
@auth.route('/sign-up', methods=['GET', 'POST']) 
@cross_origin()
def sign_up():
    if request.method == 'POST':
        data = request.json

        email = data.get('email')
        username = data.get('username')
        password1 = data.get('password1')
        password2 = data.get('password2')

        # Validate the input data
        if not email or len(email) < 4:
            return jsonify(message='Email must be provided and greater than 3 characters.'), 400
        elif not username or len(username) < 2:
            return jsonify(message='Username must be provided and greater than 1 character.'), 400
        elif not password1 or not password2 or password1 != password2:
            return jsonify(message="Passwords must be provided and must match."), 400
        elif len(password1) < 7:
            return jsonify(message='Password must be at least 7 characters.'), 400

        # Check if the username or email already exists
        
        user = User.query.filter_by(username=username).first()
        if user is not None:
            return jsonify(message='This username is already taken, try again with another username!'), 400

        user = User.query.filter_by(email=email).first()
        if user is not None:
            return jsonify(message='This email already exists, try again with another email!'), 400
        # Create a new user and save it to the database
        new_user = User(username=username, email=email, password=generate_password_hash(password1, method='sha256'))
        db.session.add(new_user)
        db.session.commit()
        user_id = new_user.id
        username = new_user.username
        email=new_user.email

        # Close db
        db.session.close()

        return jsonify({'user_id': user_id,'email': email, 'username': username})

    return jsonify({'message': 'Invalid request'}), 400


@cross_origin()
@auth.route('/logout', methods=['POST'])
def logout():
    
    return {'message': 'Logout successful'}, 200


@cross_origin()
@auth.route('/@me')
def get_current_user(): 
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    user = User.query.filter_by(id=user_id).first()
    
    response = {
            'message': f'Login successful. Welcome back {user.username}!',
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'status_code': 200
        }
    return jsonify(response), 200
