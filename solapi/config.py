class SolApiConfig:
    def __init__(self, api_key: str, secret_key: str, protocol: str = "https", domain: str = "api.solapi.com", prefix: str = ""):
        self.api_key = api_key
        self.secret_key = secret_key
        self.protocol = protocol
        self.domain = domain
        self.prefix = prefix

    def get_url(self, path: str) -> str:
        return f"{self.protocol}://{self.domain}{self.prefix}{path}"