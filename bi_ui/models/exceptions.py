class ApiError(Exception):
    """ We use ApiError to encapsulate any 400/404/500 etc. errors from an external API """
    def __init__(self, response):
        self.url = response.url
        self.status_code = response.status_code
        self.message = response.text
