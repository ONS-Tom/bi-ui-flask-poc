import logging

from flask import Blueprint, render_template


logger = logging.getLogger(__name__)
error_bp = Blueprint('error_bp', __name__, template_folder='templates/errors')


@error_bp.route('/NotFound', methods=['GET'])
def not_found_error():
    return render_template('errors/not_found.html')

