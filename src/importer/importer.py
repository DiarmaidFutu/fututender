from dataclasses import dataclass
import json
import time
from models.tender import Tender, save_tenders
import requests
from datetime import datetime
from pathlib import Path


@dataclass
class ApiCallConfig:
    server: str = "https://api.ted.europa.eu"
    path: str = "/v3/notices/search"
    limit: int = 100
    sleep: int = 0


# source: https://ec.europa.eu/eurostat/web/gisco/geodata/statistical-units/territorial-units-statistics
json_file_path = "NUTS_LB_2024_3035.geojson"
file_path = Path(__file__).parent / json_file_path
with open(file_path, "r") as file:
    nuts_data = json.load(file)


def resolve_nuts(nuts_id: str):
    for feature in nuts_data["features"]:
        if feature["properties"]["NUTS_ID"] == nuts_id:
            # print(feature["properties"])
            return (
                feature["properties"]["NAME_LATN"]
                # + ", "
                # + feature["properties"]["CNTR_CODE"]
            )
    return None


RELEVANT_FIELDS = [
    "ND",
    "publication-date",
    "buyer-name",
    "place-of-performance",
    "notice-title",
    "contract-nature",
    "links",
    "deadline",
    "total-value",
    "total-value-cur",
]


def fetch_page(config: ApiCallConfig, token=None):
    url = config.server + config.path
    payload = {
        "query": "place-of-performance IN (DE2 DE3 DE1) AND classification-cpv IN (48000000 72100000 72210000 72220000 72232000 72240000 72250000 72260000 72300000 72400000 72500000 72600000 72700000 72800000 72900000 73120000 73200000 73300000) AND submission-language IN (ENG DEU FIN) AND form-type IN (planning) SORT BY publication-number DESC",
        "fields": RELEVANT_FIELDS,
        "paginationMode": "ITERATION",
        "limit": config.limit,
        # "checkQuerySyntax": True,
    }
    if token:
        payload["iterationNextToken"] = token
    response = requests.post(url, json=payload)
    return response.json()


def fetch_data(config: ApiCallConfig):
    all_responses = []
    token = None
    has_more_results = True

    while has_more_results:
        response = fetch_page(config, token)
        all_responses += response["notices"]
        has_more_results = len(response["notices"]) == config.limit
        token = response.get("iterationNextToken")
        if (not token) or (not has_more_results):
            break
        # there is a rate limiter in place that will kick in after a few requests
        if config.sleep > 0:
            time.sleep(config.sleep)

    return all_responses


def select_with_fallback(dict: dict, *keys: list[str]) -> any:
    for key in keys:
        if key in dict:
            return dict[key]
    return None


def extract_link(links) -> str:
    return select_with_fallback(links["html"], "ENG", "GER", "FIN")


def make_unique(lst: list) -> list:
    return list(set(lst))


def contains_digits(s: str) -> bool:
    return any(char.isdigit() for char in s)


def determine_country(place_of_performance) -> str:
    countries = [
        entry
        for entry in make_unique(place_of_performance)
        if not contains_digits(entry)
    ]
    return " & ".join(countries)


def determine_region(place_of_performance) -> str:
    countries = [
        resolve_nuts(entry)
        for entry in make_unique(place_of_performance)
        if contains_digits(entry)
    ]
    return countries


def parse_publication_date(date_str: str | None) -> datetime:
    if date_str is None:
        return None
    return (
        datetime.strptime(date_str, "%Y-%m-%d%z").astimezone().replace(tzinfo=None)
    )  # .astimezone()


def parse_deadline(date_str: str | None) -> datetime:
    if date_str is None:
        return None
    return (
        datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S%z")
        .astimezone()
        .replace(tzinfo=None)
    )  #


def sanitize(notice) -> Tender:
    return Tender(
        id=notice["ND"],
        publication_date=parse_publication_date(notice["publication-date"]),
        buyer_name="".join(
            select_with_fallback(notice["buyer-name"], "eng", "deu", "fin")
        ),
        country=determine_country(notice["place-of-performance"]),
        regions=determine_region(notice["place-of-performance"]),
        # region["NUTSCode"] for region in notice["placeOfPerformance"]["regions"]
        title=select_with_fallback(notice["notice-title"], "eng", "deu", "fin"),
        type=" - ".join(make_unique(notice["contract-nature"])),
        link=extract_link(notice["links"]),
        deadline=parse_deadline(notice.get("deadline") and notice.get("deadline")[0]),
        amount=notice.get("total-value"),
        currency=notice.get("total-value-cur") and notice.get("total-value-cur")[0],
    )


def tenderize(config: ApiCallConfig) -> list[Tender]:
    results = fetch_data(config)
    return list(map(sanitize, results))


async def tenderize_and_save():
    config = ApiCallConfig()
    tenders = tenderize(config)
    return await save_tenders(tenders)
