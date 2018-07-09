import logging

from flask import flash, redirect, url_for

from bi_ui import app


logger = logging.getLogger(__name__)


@app.errorhandler(404)
def not_found_error(error):  # pylint: disable=unused-argument
    return redirect(url_for('error_bp.not_found_error'))
