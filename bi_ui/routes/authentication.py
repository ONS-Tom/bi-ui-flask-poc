from flask import Blueprint, redirect, url_for
from flask_login import login_required, current_user, logout_user


authentication_bp = Blueprint('authentication_bp', __name__, static_folder='static', template_folder='templates')


@authentication_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    user = current_user
    user.authenticated = False
    logout_user()
    return redirect(url_for('login_bp.login'))
