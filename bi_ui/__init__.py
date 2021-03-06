import os
import logging

from structlog import wrap_logger

from flask import Flask, redirect, request, url_for
from flask_login import LoginManager

from flask_session import Session
from bi_ui.models.user import User, users
from bi_ui.models.exceptions import InvalidEnvironment, MissingEnvironmentVariable, ApiError
from bi_ui.services.gateway_authentication_service import GatewayAuthenticationService

logger = wrap_logger(logging.getLogger(__name__))


app = Flask(__name__)


# Exit the program if an invalid environment is passed in
environment = os.getenv('ENVIRONMENT')  # DEV/TEST/PROD
if environment is None or environment not in ['DEV', 'TEST', 'PROD']:
    raise InvalidEnvironment(environment)

formatted_env = environment.lower().title()  # DEV -> Dev, use same format as class name
app_config = f"config.{formatted_env}Config"
app.config.from_object(app_config)  # Load config class from root of repository

# If we are in PROD, we want to fail fast if any config is missing
if environment == 'PROD':
    missing_vars = [var for var in app.config['REQUIRED_VARS'] if app.config.get(var) is None]
    if missing_vars:
        raise MissingEnvironmentVariable(missing_vars)

log_level = app.config['LOG_LEVEL']
logging.basicConfig(level=log_level, format='%(message)s')
logger.info('Log level set', log_level=log_level)
logger.info('Loaded configuration successfully', app_config=app_config)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id) -> User:
    maybe_user = next((user for user in users if user.id == user_id), None)
    return maybe_user


@app.before_request
def clear_trailing():
    """ Remove trailing slashes: https://stackoverflow.com/a/40365514 """
    rp = request.path
    if rp != '/' and rp.endswith('/'):
        return redirect(rp[:-1])


app.url_map.strict_slashes = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)


def url_for_other_page(page):
    """ This is for pagination, we need to redirect the user to the search_businesses blueprint"""
    args = request.view_args.copy()
    args['page'] = page
    return url_for('api_bp.search_businesses', **args)


app.jinja_env.globals['url_for_other_page'] = url_for_other_page


import bi_ui.views  # NOQA # pylint: disable=wrong-import-position
import bi_ui.routes  # NOQA # pylint: disable=wrong-import-position
import bi_ui.error_handlers  # NOQA # pylint: disable=wrong-import-position
