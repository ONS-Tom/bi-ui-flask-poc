from flask import Blueprint, render_template


login_bp = Blueprint('login_bp', __name__, static_folder='static', template_folder='templates')


@login_bp.route('/', methods=['GET'])
def login():
    error = None
    return render_template('login.html', error=error)
