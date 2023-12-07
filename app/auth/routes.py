from flask import render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from app.models.user import User
from app.extensions import db
from . import bp

#-----------signup route-----------
@bp.route('/signup')
def signup():
    return render_template('auth/signup.html')

@bp.route('/signup', methods=['POST'])
def signup_post():
    #handling the POST form data
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    location = request.form.get('location')

    user=User.query.filter_by(email=email).first()
    if user:
        return redirect(url_for('auth.signup'))
    
    new_user=User(name=name, email=email, password=generate_password_hash(password, method='pbkdf2:sha256'), location=location)

    db.session.add(new_user)
    db.session.commit()

    flash('Email address already exists')
    return redirect(url_for('auth.login'))

#-----------login route------------
@bp.route('/login')
def login():
    return render_template('auth/login.html')

@bp.route('/login', methods=['POST'])
def login_post():
    # login code
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again')
        return redirect(url_for('auth.login'))

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))

#-----------logout-------------
@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))