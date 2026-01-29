from typing import List
from mutagen import File

TAGS_PRIORITY_ORDER = ["title", "album", "albumartist", "artist"]

def raw_search_query(song_path: str, tags_to_include: List[str] = None) -> str:
    """
    Build a search query string from selected audio tags.

    Args:
        song_path: Path to the audio file.
        tags_to_include: Default ['title', 'album'] for search.
            Additional options - 'artist', 'albumartist'.

    Returns:
        Formatted search query string.
    """

    # set default tags to include
    if tags_to_include is None:
        tags_to_include = ['title', 'album']
    else:
        for i in range(len(tags_to_include)):
            tags_to_include[i] = tags_to_include[i].lower()

    audio = File(song_path)

    raw_query = ""
    # add to raw_query by priority
    for tag in TAGS_PRIORITY_ORDER:
        if tag in tags_to_include:
            for key, value in audio.tags.items():
                if key == tag:
                    raw_query += value[0] + " "

    # print(raw_query)
    return raw_query

raw_search_query(song_path="C:\\Users\\Max\\Desktop\\music\\Various Interprets - Ha Raham (Mehfuz).flac", tags_to_include=['albUm', 'albumArtIst', 'Title', 'arTist'])