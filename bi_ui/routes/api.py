import logging
from structlog import wrap_logger
from flask import Blueprint, request, flash, redirect, url_for, session
from flask_login import login_required

from bi_ui.services.business_service import BusinessService
from bi_ui.models.exceptions import ApiError
from bi_ui.utilities.sic_codes import industry_code_description
from bi_ui.utilities.convert_bands import employment_bands, legal_status_bands, turnover_bands, trading_status_bands
from bi_ui.utilities.helpers import compose, convert_band, highlight
from bi_ui.models.pagination import Pagination

logger = wrap_logger(logging.getLogger(__name__))


api_bp = Blueprint('api_bp', __name__, static_folder='static', template_folder='templates')


business_service = BusinessService()


PAGE_SIZE = 5  # This should be moved into config


sic = lambda business: convert_band(business, 'IndustryCode', 'industry code description', industry_code_description)
trading_status = lambda business: convert_band(business, 'TradingStatus', 'trading status', trading_status_bands)
legal_status = lambda business: convert_band(business, 'LegalStatus', 'legal status', legal_status_bands)
employment_band = lambda business: convert_band(business, 'EmploymentBands', 'employment band', employment_bands)
turnover_band = lambda business: convert_band(business, 'Turnover', 'turnover band', turnover_bands)


@api_bp.route('/search_businesses', methods=['POST', 'GET'])
@login_required
def search_businesses(business_name=None):
    page = int(request.args.get('page', 1))

    if request.method == 'GET':
        business_name = session['business_name']

    fro = (page - 1) * PAGE_SIZE
    size = page * PAGE_SIZE
    if not business_name:
        business_name = request.form['BusinessName']
    query = f'BusinessName:{business_name}&from={fro}&size={size}'
    try:
        num_results, json = business_service.search_businesses(query)
    except (ApiError, ValueError) as e:
        logger.error('Unable to return Business search results')
        raise e

    # Save the query in the session, so we can implement pagination
    session['business_name'] = business_name

    convert_bands = compose(sic, trading_status, legal_status, employment_band, turnover_band)
    highlighted = [highlight(business, business_name) for business in json]
    businesses = list(map(convert_bands, highlighted))

    pagination = Pagination(int(page), int(5), int(num_results))
    session['pagination'] = pagination

    # We will implement pagination later, for now we can just pass a subset of the results
    flash([num_results, businesses])
    return redirect(url_for('results_bp.results', page=page))

