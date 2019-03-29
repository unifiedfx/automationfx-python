from requests.auth import AuthBase

class APIKeyAuth(AuthBase):
    """Attaches APIKey Authentication to the given Request object."""
    apikey = ""
    def __init__(self, apikey):
        # setup any auth-related data here
        self.apikey = apikey

    def __call__(self, r):
        # modify and return the request
        r.headers['Apikey'] = self.apikey
        return r
