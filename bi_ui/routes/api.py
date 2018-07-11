import logging
from flask import Blueprint, request, flash, redirect, url_for
from flask_login import login_required

from bi_ui.services.business_service import BusinessService
from bi_ui.models.exceptions import ApiError
from bi_ui.utilities.sic_codes import industry_code_description
from bi_ui.utilities.convert_bands import employment_bands, legal_status_bands, turnover_bands, trading_status_bands
from bi_ui.utilities.helpers import compose, convert_band


logger = logging.getLogger(__name__)


api_bp = Blueprint('api_bp', __name__, static_folder='static', template_folder='templates')


business_service = BusinessService()


sic = lambda business: convert_band(business, 'IndustryCode', 'industry code description', industry_code_description)
trading_status = lambda business: convert_band(business, 'TradingStatus', 'trading status', trading_status_bands)
legal_status = lambda business: convert_band(business, 'LegalStatus', 'legal status', legal_status_bands)
employment_band = lambda business: convert_band(business, 'EmploymentBands', 'employment band', employment_bands)
turnover_band = lambda business: convert_band(business, 'Turnover', 'turnover band', turnover_bands)


@api_bp.route('/search_businesses', methods=['POST'])
@login_required
def search_businesses():
    business_name = request.form['BusinessName']
    try:
        json = business_service.search_businesses(f'BusinessName:{business_name}')
    except (ApiError, ValueError) as e:
        logger.exception('Unable to return Business search results', e)
        raise e

    json_subset = json[0:5]

    convert_bands = compose(sic, trading_status, legal_status, employment_band, turnover_band)
    businesses = list(map(convert_bands, json_subset))

    # We will implement pagination later, for now we can just pass a subset of the results
    flash([148, businesses])
    return redirect(url_for('results_bp.results'))
