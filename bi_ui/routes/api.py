import logging
from structlog import wrap_logger
from flask import Blueprint, request, redirect, url_for, session
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


# Need to look at where to store these, for internationalisation etc.
ERROR_MESSAGES = {
    404: 'The search query you entered did not return any results.',
    500: 'An error occurred. Please contact your system administrator.',
    503: 'An error occurred. This is likely to be an issue with ElasticSearch.',
    504: 'An error occurred. This is likely to be a timeout issue.'
}

ERROR_CODES = {
    404: 'Not Found',
    500: 'Internal Server Error',
    503: 'Service Unavailable',
    504: 'Gateway Timeout'
}


@api_bp.errorhandler(ApiError)
def handle_error(error: ApiError):
    error_code_detail = ERROR_CODES.get(error.status_code, 'Error')
    session['level'] = 'warn' if error.status_code == 404 else 'error'
    session['title'] = f'{error.status_code} - {error_code_detail}'
    session['error_message'] = ERROR_MESSAGES.get(error.status_code, 'An error occurred.')
    return redirect(url_for('error_bp.error'))


sic = lambda business: convert_band(business, 'IndustryCode', 'industry code description', industry_code_description)
trading_status = lambda business: convert_band(business, 'TradingStatus', 'trading status', trading_status_bands)
legal_status = lambda business: convert_band(business, 'LegalStatus', 'legal status', legal_status_bands)
employment_band = lambda business: convert_band(business, 'EmploymentBands', 'employment band', employment_bands)
turnover_band = lambda business: convert_band(business, 'Turnover', 'turnover band', turnover_bands)


@api_bp.route('/search_businesses', methods=['POST', 'GET'])
@login_required
def search_businesses(business_name=None):
    # The page request arg is set by our global pagination method for use in the pagination macro
    page = int(request.args.get('page', 1))

    # This is to handle when the pagination buttons are pressed
    if request.method == 'GET':
        business_name = session['business_name']

    fro = (page - 1) * PAGE_SIZE
    if not business_name:
        business_name = request.form['BusinessName']
    query = f'BusinessName:{business_name}&from={fro}&size={PAGE_SIZE}'
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

    # We need to use the capped number of results for the pagination, or else there will be too many pages
    capped_num_results = 10000 if int(num_results) > 10000 else int(num_results)
    pagination = Pagination(int(page), int(5), int(capped_num_results))

    session['pagination'] = pagination
    session['num_results'] = num_results
    session['businesses'] = businesses
    return redirect(url_for('results_bp.results', page=page))

