from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import requests
import random
from utils.helpers import human_delay, extract_lrclib_lyrics, build_search_query, match_song_metadata, get_songs
import time
import logging
import json
from typing import Tuple, Optional

log = logging.getLogger(__name__)


UA_POOL = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
]

BASE_HEADERS = {
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "close",
}


LRCLIB_SEARCH_URL = "https://lrclib.net/api/search"
SESSION_ROTATE_EVERY = 10
MAX_SEARCH_ATTEMPTS = 3


def _build_session() -> requests.Session:
    retry = Retry(
        total=3,
        connect=3,
        read=3,
        backoff_factor=1.2,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods={"GET"},
        raise_on_status=False,
    )

    adapter = HTTPAdapter(max_retries=retry)

    s = requests.Session()
    s.mount("https://", adapter)
    s.headers.update(BASE_HEADERS)
    s.headers["User-Agent"] = random.choice(UA_POOL)
    return s


_session: requests.Session = _build_session()
_request_count = 0


def _rotate_session(force: bool = False) -> False:
    global _session, _request_count
    if force or _request_count >= SESSION_ROTATE_EVERY:
        try:
            _session.close()
        finally:
            _session = _build_session()
            _request_count = 0


def _safe_get(params: dict) -> Optional[list]:
    global _request_count
    _request_count += 1

    try:
        r = _session.get(
            LRCLIB_SEARCH_URL,
            params=params,
            timeout=(4, 12),
        )
    except requests.exceptions.SSLError:
        _rotate_session(force=True)
        return False
    except requests.exceptions.RequestException:
        return False

    if r.status_code == 429:
        time.sleep(random.uniform(30, 60))
        return False

    if r.status_code != 200:
        return False

    try:
        return r.json()
    except ValueError:
        return False


def fetch_lyrics(song_path: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Returns (synced_lyrics, unsynced_lyrics)
    """

    synced = False
    unsynced = False

    search_queries = build_search_query(song_path)
    if isinstance(search_queries, str):
        search_queries = [search_queries]

    for attempt in range(MAX_SEARCH_ATTEMPTS):
        for query in search_queries:
            json_data = _safe_get(
                {
                    "q": query,
                    "limit": 20,
                }
            )

            if not json_data:
                continue

            (
                synced_lrc,
                synced_desc,
                unsynced_lrc,
                unsynced_desc,
            ) = extract_lrclib_lyrics(json_data=json_data)

            try:
                if synced_lrc and synced_desc:
                    if match_song_metadata(
                        local_song_path=song_path,
                        received_song_info=synced_desc,
                        threshold=65,
                        print_match=False,
                    ):
                        synced = synced_lrc

                if unsynced_lrc and unsynced_desc:
                    if match_song_metadata(
                        local_song_path=song_path,
                        received_song_info=unsynced_desc,
                        threshold=65,
                        print_match=False,
                    ):
                        unsynced = unsynced_lrc
            except Exception:
                pass

            if synced or unsynced:
                return synced, unsynced

        time.sleep(random.uniform(0.8, 1.5))
        _rotate_session()

    return False, False



if __name__ == "__main__":
    MUSIC_DIRECTORY = "C:\\Users\\Max\\Desktop\\music\\small"
    music_files = get_songs(music_dir=MUSIC_DIRECTORY)

    for i, song_path in enumerate(music_files):
        print(f"{i+1}. {song_path.stem}")
        synced, unsynced =  fetch_lyrics(song_path=song_path)
        if synced is False: print(f"synced: False")
        if unsynced is False: print(f"unsynced: False")
        underline = "‾" * len(song_path.stem)
        with open(f"lyrics/{song_path.stem}.lrc", "w", encoding="utf-8") as f:
            f.write(f"{song_path.stem}\n{underline}\n{synced}")
            f.write(f"\n\n{song_path.stem}\n{underline}\n{unsynced}")

