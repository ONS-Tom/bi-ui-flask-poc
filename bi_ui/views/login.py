import uuid
from flask import Blueprint, render_template, request, redirect, url_for
from bi_ui.models.user import User
from flask_login import login_user


login_bp = Blueprint('login_bp', __name__, static_folder='static', template_folder='templates')


@login_bp.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == 'admin' and password == 'admin':
            id = str(uuid.uuid4())
            user = User(id)
            login_user(user)
            return redirect(url_for('home_bp.home'))
        else:
            error = 'Invalid Credentials. Please try again.'

            # if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            #     error = 'Invalid Credentials. Please try again.'
            # else:
            #     login_user(user)
            #     return redirect(url_for('.home'))
    return render_template('login.html', error=error)
