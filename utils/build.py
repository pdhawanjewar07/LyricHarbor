from typing import List
from mutagen import File

TAGS_PRIORITY_ORDER = ["title", "artist", "album"]

def raw_search_query(song_path: str, source:str) -> str:
    """
    Build a search query string from selected audio tags.

    Args:
        song_path: Path to the audio file.
        source: lyrics provider

    Returns:
        Formatted search query string.
    """

    # set default tags to include
    match source:
        case "musixmatch-via-spotify":
            tags_to_include = ['title', 'artist']
        case "lrclib":
            tags_to_include = ['title', 'artist', 'album']
        case _: 
            tags_to_include = ['title', 'artist']


    audio = File(song_path)

    raw_query = ""
    # add to raw_query by priority
    for tag in tags_to_include:
        for key, value in audio.tags.items():
            if key == tag:
                raw_query += value[0] + " "

    # print(raw_query)
    return raw_query

# raw_search_query(song_path="C:\\Users\\Max\\Desktop\\music\\Anuj Gurwara - Thoda Hans Ke.flac")