from typing import List
from mutagen import File

TAGS_PRIORITY_ORDER = ["title", "artist", "albumartist" "album"]

def raw_search_query(song_path: str, source:int) -> str:
    """
    Build a search query string from selected audio tags.

    Args:
        song_path: Path to the audio file.
        source: lyrics provider[musixmatch-via-spotify(0), lrclib(1), genius(2)]

    Returns:
        Raw search query(str).
    """

    # set default tags to include
    match source:
        case 0: # musixmatch-via-spotify
            tags_to_include = ['title', 'artist', 'album']
        case 1: # lrclib
            tags_to_include = ['title', 'artist', 'album']
        case 2: # genius
            tags_to_include = ['title', 'albumartist']
        case _: # default
            tags_to_include = ['title', 'artist', 'album']


    audio = File(song_path)

    raw_query = ""
    # add to raw_query by priority
    for tag in tags_to_include:
        for key, value in audio.tags.items():
            if key == tag:
                raw_query += value[0] + " "

    # print(raw_query)
    return raw_query

# raw_search_query(song_path="C:\\Users\\Max\\Desktop\\music\\Anuj Gurwara - Thoda Hans Ke.flac", source=0)