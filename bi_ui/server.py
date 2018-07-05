import logging
import uuid

from flask import Flask, render_template, redirect, url_for, request, abort
from flask_login import LoginManager, login_required, login_user

from flask_session import Session
from .models.user import User

logger = logging.getLogger(__name__)


def create_app():
    app = Flask(__name__)
    return app


login_manager = LoginManager()
app = create_app()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


@app.route('/Login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == 'admin' and password == 'admin':
            id = str(uuid.uuid4())
            user = User(id)
            login_user(user)
            # return redirect(request.args.get("next"))
            return redirect(url_for('.home'))
        else:
            error = 'Invalid Credentials. Please try again.'

            # if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            #     error = 'Invalid Credentials. Please try again.'
            # else:
            #     login_user(user)
            #     return redirect(url_for('.home'))
    return render_template('login.html', error=error)


@app.route('/Home')
@login_required
def home():
    return 'Home Page'


@app.route('/Results')
@login_required
def results():
    return 'Results Page'


@app.route('/NotFound')
def not_found():
    return 'Not Found'


app.secret_key = 'change_me'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
