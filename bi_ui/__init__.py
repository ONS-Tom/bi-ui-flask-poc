import logging

from flask import Flask, redirect, request
from flask_login import LoginManager

from flask_session import Session
from bi_ui.models.user import User


logger = logging.getLogger(__name__)


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


@app.before_request
def clear_trailing():
    """ Remove trailing slashes: https://stackoverflow.com/a/40365514 """
    rp = request.path
    if rp != '/' and rp.endswith('/'):
        return redirect(rp[:-1])


app.url_map.strict_slashes = False
app.secret_key = 'change_me'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)


import bi_ui.views  # NOQA # pylint: disable=wrong-import-position
import bi_ui.error_handlers  # NOQA # pylint: disable=wrong-import-position
