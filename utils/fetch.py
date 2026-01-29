import requests
import time
import random
import json
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Human-like timing
def human_delay(min_s:float=9.0, max_s:float=15.0):
    sleep_time = random.uniform(min_s, max_s)
    print(f"waiting - {sleep_time:.3f} seconds")
    time.sleep(sleep_time)

# One global session (safe)
_session = requests.Session()

_retry = Retry(
    total=2,
    backoff_factor=1.5,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET"],
    raise_on_status=False,
)

_adapter = HTTPAdapter(
    max_retries=_retry,
    pool_connections=1,
    pool_maxsize=1
)

_session.mount("https://", _adapter)

_session.headers.update({
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
})

# Optimized function
def lyrics(search_query: str, mode: int = 2) -> list | None:
    """
    Fetch lyrics metadata from lrclib.

    Returns:
        Json list if found, otherwise None.
    """

    human_delay(2.5, 6.0)

    response = _session.get(
        "https://lrclib.net/api/search",
        params={
            "q": search_query,
            "limit": random.choice([10, 15, 20])
        },
        timeout=(3, 10),
        allow_redirects=True
    )

    human_delay(2.0, 4.5)

    if response.status_code != 200:
        return None

    data = response.json()

    if not isinstance(data, list) or not data:
        return None

    human_delay(6.0, 12.0)

    return data



query_list = [
    "Chokra Jawaan Ishaqzaade Amit Trivedi Vishal Dadlani Sunidhi Chauhan Habib Faisal",
    "Bezubaan Phir Se ABCD 2",
    "Jaane Bhi De Heyy Babyy Shankar Mahadevan",
    "Ha Raham Mehfuz Aamir Original Motion Picture Soundtrack Amit Trivedi"
]
for index, query in enumerate(query_list):
    print(f"starting - {index+1}")
    data = lyrics(search_query=query, mode=2)
    # Overwrite file every call (explicit, safe)
    with open(f"response{index}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

