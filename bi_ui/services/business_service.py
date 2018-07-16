import logging
import requests
from structlog import wrap_logger
from typing import List, Tuple, Optional

from bi_ui.models.exceptions import ApiError
from bi_ui.utilities.helpers import log_api_error


logger = wrap_logger(logging.getLogger(__name__))


class BusinessService:
    NumResults = Optional[int]
    Business = dict
    Businesses = List[Business]
    SearchResponse = Tuple[NumResults, Businesses]

    def __init__(self):
        self.base_url = 'http://localhost:9000'
        self.version = 'v1'

    def get_business_by_id(self, business_id: str) -> Business:
        response = requests.get(f'{self.base_url}/{self.version}/business/{business_id}')

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            log_api_error(response.status_code, 'Failed to retrieve Business', business_id)
            raise ApiError(response)

        return response.json()  # Can throw ValueError

    def search_businesses(self, query) -> SearchResponse:
        response = requests.get(f'{self.base_url}/{self.version}/search/{query}')

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            log_api_error(response.status_code, 'Failed to search Businesses', query)
            raise ApiError(response)

        return response.headers.get('X-Total-Count'), response.json()  # Can throw ValueError

