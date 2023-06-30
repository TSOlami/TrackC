from flask import Blueprint,  render_template, request, flash, make_response, redirect, url_for
from .models import *
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user,login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST']) 
def login():
    """Endpoint to handle User login"""
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
        elif not username or len(username) < 2:
            flash('Username must be greater than 1 character.', category='error')
        elif not password1 or not password2 or password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')

        # Check if the username or email already exists
        
        user = User.query.filter_by(username=username).first()
        if user is not None:
            flash('This username is already taken, try again with another username!', category='error')

        user = User.query.filter_by(email=email).first()
        if user is not None:
            flash('This email is already taken, try again with another email!', category='error')
        # Create a new user and save it to the database
        new_user = User(username=username, email=email, password=generate_password_hash(password1, method='sha256'))
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully, Welcome {}!'.format(user.username), category='success')
        user_id = new_user.id
        username = new_user.username
        email=new_user.email

        # Close db
        db.session.close()

        return redirect(url_for('views.home', user_id=user_id))

    return render_template("sign_up.html", user=current_user)


@auth.route('/logout', methods=['POST'])
def logout():
    
    return {'message': 'Logout successful'}, 200


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
