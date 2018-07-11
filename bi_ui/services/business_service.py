import logging
import requests
from structlog import wrap_logger
from typing import List, Tuple, Optional

from bi_ui.models.exceptions import ApiError


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


def log_api_error(status: int, error_msg: str, query: str):
    """ log """
    if status == 404:
        logger.info(error_msg, status=status, query=query)
    elif status == 400:
        logger.warning(error_msg, status=status, query=query)
    elif status == 500:
        logger.error(error_msg, status=status, query=query)
