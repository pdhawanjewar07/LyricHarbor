import logging
from utils.fetch import lrclib, genius, musixmatch
from enum import IntEnum
from typing import Iterable, Callable

log = logging.getLogger(__name__)

class LyricsMode(IntEnum):
    SYNCED_ONLY = 0
    UNSYNCED_ONLY = 1
    SYNCED_FALLBACK = 2


SOURCE_FETCHERS = {
    "musixmatch-via-spotify": {
        "synced": lambda song_path: musixmatch.fetch_lyrics(song_path, mode=0),
        "unsynced": lambda song_path: musixmatch.fetch_lyrics(song_path, mode=1),
    },
    "lrclib": {
        "synced": lambda song_path: lrclib.fetch_lyrics(song_path, mode=0),
        "unsynced": lambda song_path: lrclib.fetch_lyrics(song_path, mode=1),
    },
    "genius": {
        "unsynced": lambda song_path: genius.fetch_lyrics(song_path),
    },
}


def _try_fetch(
    song_path: str,
    sources: Iterable[str],
    kind: str,  # "synced" | "unsynced"
):
    for source in sources:
        fetcher: Callable | None = SOURCE_FETCHERS.get(source, {}).get(kind)
        if not fetcher:
            continue
        lyrics = fetcher(song_path)
        if lyrics:
            return lyrics
    return False


def fetch_lyrics(
    song_path: str,
    lyrics_fetch_mode: LyricsMode,
    lyrics_sources: Iterable[str],
):
    if not lyrics_sources:
        return False

    if lyrics_fetch_mode == LyricsMode.SYNCED_ONLY:
        return _try_fetch(song_path, lyrics_sources, "synced")

    if lyrics_fetch_mode == LyricsMode.UNSYNCED_ONLY:
        return _try_fetch(song_path, lyrics_sources, "unsynced")

    # SYNCED_FALLBACK
    synced = _try_fetch(song_path, lyrics_sources, "synced")
    if synced:
        return synced

    return _try_fetch(song_path, lyrics_sources, "unsynced")