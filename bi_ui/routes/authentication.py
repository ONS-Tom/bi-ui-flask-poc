import uuid
from flask import Blueprint, redirect, url_for, request, flash
from flask_login import login_required, current_user, logout_user, login_user
from bi_ui.models.user import User


authentication_bp = Blueprint('authentication_bp', __name__, static_folder='static', template_folder='templates')


@authentication_bp.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username == 'admin' and password == 'admin':
        id = str(uuid.uuid4())
        user = User(id)
        login_user(user)
        return redirect(url_for('home_bp.home'))
    else:
        flash('Invalid Credentials. Please try again.')
        return redirect(url_for('login_bp.login'))


@authentication_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    user = current_user
    user.authenticated = False
    logout_user()
    return redirect(url_for('login_bp.login'))
