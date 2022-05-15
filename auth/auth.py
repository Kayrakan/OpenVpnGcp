
from flask import Blueprint, render_template, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from openvpn.models import User
from openvpn import db
from flask_login import login_user,login_required, logout_user


user_management = Blueprint('auth', __name__, static_folder='static', template_folder='templates')


@user_management.route('/login')
def login():
    return render_template('login.html')

@user_management.route('/login', methods=['POST'])
def login_post():
    # login code goes here
    # login code goes here
    print('logged in')
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    print(User.query.all())
    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

    login_user(user, remember=remember)

    # if the above check passes, then we know the user has the right credentials
    return redirect(url_for('profile'))

@user_management.route('/signup')
def signup():
    return render_template('signup.html')

@user_management.route('/signup', methods=['POST'])
def signup_post():
    # code to validate and add user to database goes here
    print('requested')
    print(request.data)
    print(request.form.get('email'))
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
    print('saving')

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))


@user_management.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))