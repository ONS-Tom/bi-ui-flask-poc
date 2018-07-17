from flask import Blueprint, render_template, session
from flask_login import login_required


results_bp = Blueprint('results_bp', __name__, static_folder='static', template_folder='templates')


@results_bp.route('/Page/<int:page>', methods=['GET'])
@login_required
def results(page):
    pagination = session['pagination']
    return render_template('results.html', pagination=pagination)
