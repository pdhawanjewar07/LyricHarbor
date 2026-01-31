import json
from pathlib import Path

def synced(json_data:list[dict]) -> str|bool:
    """
    Returns:
        synced lyrics(str) if found, otherwise False
    """
    if not isinstance(json_data, list):
        return False

    for item in json_data:
        synced_lyrics = item.get("syncedLyrics")
        if  synced_lyrics == None:
            pass
        else:
            return synced_lyrics

    return False

def unsynced(json_data:list[dict]) -> str|bool:
    """
    Returns:
        unsynced lyrics(str) if found, otherwise False
    """
    if not isinstance(json_data, list):
        return False

    for item in json_data:
        unsynced_lyrics = item.get("plainLyrics")
        if  unsynced_lyrics == None:
            pass
        else:
            return unsynced_lyrics
    return False

def save(lyrics:str, out_dir: str, out_filename:str):
    lyrics_file = out_dir + f"\\{out_filename}.lrc"
    with open(lyrics_file, "w", encoding="utf-8") as f:
        f.write(lyrics)
    return True

def lyrics(json_data: list[dict], out_dir: str, out_filename:str, mode: int = 2) -> int:
    """
    extract lyrics from json data and save to given location

    Args:
        data: json data(response) recieved from api request
        out_dir: output location for lyrics
        out_filename: output file name to be saved as
        mode: synced(0), unsynced(1), synced_with_fallback(2)

    Returns:
        0
    """

    if not json_data:
        return False

    match mode:
        case 0: # synced only
            lyrics = synced(json_data=json_data)
            if lyrics:
                save(lyrics=lyrics, out_dir=out_dir, out_filename=out_filename)
                return True
        case 1: # unsynced only
            lyrics = unsynced(json_data=json_data)
            if lyrics:
                save(lyrics=lyrics, out_dir=out_dir, out_filename=out_filename)
                return True
        case 2: # synced with fallback to unsynced
            pass
        case _: # DEFAULT: synced with fallback to unsynced
            pass

    return False


"""
extract_and_save(
    data="C:\\Users\\Max\\Desktop\\VS-Code\\Github Repositories\\time-synced-lyrics\\response0.json",
    out_dir="C:\\Users\\Max\\Desktop\\VS-Code\\Github Repositories\\time-synced-lyrics\\lyrics",
    mode=0,
)
"""