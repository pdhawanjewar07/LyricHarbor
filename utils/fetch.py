import requests
import time
import random
import json
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from config import LYRICS_SOURCES
from utils.helpers import human_delay



# General Variables Declaration
UA_POOL = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
]
BASE_HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    # kill keep-alive to avoid poisoned TLS sockets
    "Connection": "close",
}
_retry = Retry(
    total=2,
    backoff_factor=1.5,
    status_forcelist=[500, 502, 503, 504],
    allowed_methods=["GET"],
    raise_on_status=False,
)

_adapter = HTTPAdapter(max_retries=_retry)

# Session factory
def new_session() -> requests.Session:
    s = requests.Session()
    s.mount("https://", _adapter)
    headers = BASE_HEADERS.copy()
    headers["User-Agent"] = random.choice(UA_POOL)
    s.headers.update(headers)
    return s


# Global session (rotated)
_session = new_session()
_request_count = 0
SESSION_ROTATE_EVERY = 7


# Optimized lyrics fetch
def lyrics(search_query: str) -> list | None:
    """
    Fetch lyrics metadata from lrclib.

    Args:
        search_query: cleaned search query

    Returns:
        JSON list if found, otherwise None.
    """
    global _session, _request_count

    # rotate session periodically
    _request_count += 1
    if _request_count % SESSION_ROTATE_EVERY == 0:
        try:
            _session.close()
        finally:
            _session = new_session()

    human_delay(mean=2.5)

    try:
        response = _session.get(
            "https://lrclib.net/api/search",
            params={
                "q": search_query,
                "limit": random.choice([10, 15, 20]),
            },
            timeout=(3, 10),
            allow_redirects=True,
        )

    except requests.exceptions.SSLError:
        # poisoned TLS session → hard reset
        try:
            _session.close()
        finally:
            _session = new_session()
        return None

    except requests.exceptions.RequestException:
        return None

    # explicit rate-limit handling
    if response.status_code == 429:
        time.sleep(random.uniform(60, 120))
        return None

    if response.status_code != 200:
        return None

    try:
        data = response.json()
    except ValueError:
        return None

    # small post-request pause
    human_delay(mean=3.0)

    return data




"""
query_list = [
    "Chokra Jawaan Ishaqzaade Amit Trivedi Vishal Dadlani Sunidhi Chauhan Habib Faisal",
    "Bezubaan Phir Se ABCD 2",
    "Jaane Bhi De Heyy Babyy Shankar Mahadevan",
    "Ha Raham Mehfuz Aamir Original Motion Picture Soundtrack Amit Trivedi"
]
for index, query in enumerate(query_list):
    print(f"starting - {index}")
    data = lyrics(search_query=query)
    # Overwrite file every call (explicit, safe)
    with open(f"response{index}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

"""