class ApiError(Exception):
    def __init__(self, endpoint, response_code, message=""):
        self.endpoint = endpoint
        self.response_code = response_code
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'Call to {self.endpoint} returned {self.response_code}. Reason: {self.message}'