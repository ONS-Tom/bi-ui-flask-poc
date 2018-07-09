from flask import Blueprint, render_template
from flask_login import login_required


results_bp = Blueprint('results_bp', __name__, static_folder='static', template_folder='templates')


@results_bp.route('/', methods=['GET'])
@login_required
def results():
    return render_template('results.html')
