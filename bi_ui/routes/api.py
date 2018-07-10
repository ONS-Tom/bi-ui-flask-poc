import logging
from flask import Blueprint, jsonify, request
from flask_login import login_required

from bi_ui.services.business_service import BusinessService
from bi_ui.models.exceptions import ApiError


logger = logging.getLogger(__name__)


api_bp = Blueprint('api_bp', __name__, static_folder='static', template_folder='templates')


business_service = BusinessService()


@api_bp.route('/search_businesses', methods=['POST'])
@login_required
def search_businesses():
    business_name = request.form['BusinessName']
    try:
        json = business_service.search_businesses(f'BusinessName:{business_name}')
    except (ApiError, ValueError) as e:
        logger.exception('Unable to return Business search results', e)
        raise e

    return jsonify(json)
