import logging
from structlog import wrap_logger

from flask import Blueprint, render_template, session, flash
from flask_login import login_required


logger = wrap_logger(logging.getLogger(__name__))


results_bp = Blueprint('results_bp', __name__, static_folder='static', template_folder='templates')


@results_bp.route('/Page/<int:page>', methods=['GET'])
@login_required
def results(page):
    pagination = session['pagination']
    num_results = session['num_results']
    businesses = session['businesses']
    flash([int(num_results), businesses])
    return render_template('results.html', pagination=pagination)
