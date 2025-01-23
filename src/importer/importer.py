from models.tender import Tender


class ApiCallConfig:
    server: str = "https://api.ted.europa.eu"
    path: str = "/v3/notices/search"
    limit: int = 100
    sleep: int = 0


def tenderize(config: ApiCallConfig) -> list[Tender]: ...
