import os


class DevConfig:
    """
    For the 'important' environment variables (URLs), we want to be able to 'fail-fast' if no environment
    variable has been set, so we will leave those config values as None. For non-vital config such as
    timeouts, we provide a default value.

    In the application startup code, if any None's are found in the config, the application will not start.
    """
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    API_TIMEOUT = os.getenv('API_TIMEOUT', 10)
    AUTH_TIMEOUT = os.getenv('AUTH_TIMEOUT', 10)
    AUTH_URL = os.getenv('AUTH_URL', '')
    API_URL = os.getenv('API_URL', 'http://localhost:9000')
    SECRET_KEY = os.getenv('SECRET_KEY', 'change_me')


class TestConfig(DevConfig):
    LOG_LEVEL = 'DEBUG'


class ProdConfig(DevConfig):
    REQUIRED_VARS = ['AUTH_URL', 'API_URL', 'SECRET_KEY']
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'WARNING')
    AUTH_URL = os.getenv('AUTH_URL')
    API_URL = os.getenv('API_URL')
    SECRET_KEY = os.getenv('SECRET_KEY')
