import logging
import requests
from structlog import wrap_logger
from typing import Tuple

from bi_ui.models.exceptions import ApiError
from bi_ui.utilities.helpers import log_api_error, base_64_encode


logger = wrap_logger(logging.getLogger(__name__))


class GatewayAuthenticationService:
    Role = str
    Token = str  # A uuid from the API Gateway
    TokenAndRole = Tuple[Token, Role]

    def __init__(self, gateway_auth_url: str):
        self.gateway_auth_url = gateway_auth_url

    def login(self, username: str, password: str) -> TokenAndRole:
        headers = {'content-type': 'application/json', 'Authorization': base_64_encode(f'{username}:{password}')}
        response = requests.post(self.gateway_auth_url, headers=headers)

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            log_api_error(response.status_code, 'Failed to authorize via the API Gateway', self.gateway_auth_url)
            raise ApiError(response)

        token, role = response.json()
        return token, role
