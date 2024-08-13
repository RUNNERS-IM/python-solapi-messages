class SolApiConfig:
    def __init__(self, api_key, secret_key, protocol="https", domain="api.solapi.com", prefix=""):
        self.api_key = api_key
        self.secret_key = secret_key
        self.protocol = protocol
        self.domain = domain
        self.prefix = prefix

    def get_url(self, path):
        return f"{self.protocol}://{self.domain}{self.prefix}{path}"