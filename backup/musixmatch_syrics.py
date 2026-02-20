# when using syrics

from utils.helpers import extract_spotify_lyrics, build_search_query, match_song_metadata, get_songs
import logging
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
from syrics.api import Spotify
from config import SPOTIFY_TRACK_CSS_SELECTOR
import requests
from utils.playwright_driver import PlaywrightDriver
import re
import json


load_dotenv()
SPOTIFY_DC_TOKEN = os.getenv("SP_DC_TOKEN")
log = logging.getLogger(__name__)
sp = Spotify(SPOTIFY_DC_TOKEN)


driver = PlaywrightDriver(headless=False)   # False only for debugging

def fetch_lyrics(song_path: str) -> tuple:
    """
    Fetch lyrics from musixmatch-via-spotify
    
    :param song_path: song path
    :type song_path: str
    :return: (synced_lyrics, unsynced_lyrics) items can be str|False
    :rtype: tuple

    """
    cache = {
        "synced_lyrics":False,
        "unsynced_lyrics":False
    }

    search_query = build_search_query(song_path=song_path)
    # print(f"______Search Query: {search_query}")
    search_url = f"https://open.spotify.com/search/{search_query}/tracks"
    # print(f"Spotify search url: {search_url}")

    driver.page.goto(search_url)
    driver.page.wait_for_selector(SPOTIFY_TRACK_CSS_SELECTOR)
    driver.page.click(SPOTIFY_TRACK_CSS_SELECTOR)
    driver.page.wait_for_url("**/track/**")

    spotify_track_url = driver.page.url
    # print(f"Spotify _track url: {spotify_track_url}")

    #/start For track comparison 
    resp = requests.get(spotify_track_url,headers={"User-Agent": "Mozilla/5.0"},timeout=10)
    if resp.status_code != 200: return (False, False)  

    soup = BeautifulSoup(resp.text, "html.parser")
    def meta(prop):
        tag = soup.find("meta", property=prop)
        return tag["content"] if tag else None
    
    recieved_song_title = meta("og:title")
    recieved_song_description = meta("og:description")
    recieved_song_info = f'{recieved_song_title} {recieved_song_description}'
    flag = match_song_metadata(local_song_path=song_path, received_song_info=recieved_song_info, threshold=70)
    if flag is False: return (False, False)
    print(f"flag: {flag}")
    #/end For track comparison

    match = re.search(r"/track/([A-Za-z0-9]+)", spotify_track_url)
    spotify_track_id = match.group(1)
    # print(f"Spotify track id: {spotify_track_id}")

    json_response = sp.get_lyrics(track_id=spotify_track_id)
    # save json response
    print(json_response)
    with open(f"_lyrics/{recieved_song_title}.json", "w", encoding="utf-8") as f:
        json.dump(json_response, f, ensure_ascii=False, indent=2)

    lyrics = extract_spotify_lyrics(json_data=json_response)
    print(f"lyrics: {lyrics}")
    try: 
        cache["synced_lyrics"] = lyrics[0]
        cache["unsynced_lyrics"] = lyrics[1]
    except: pass
        

    return (cache["synced_lyrics"], cache["unsynced_lyrics"])


if __name__ == "__main__":
    MUSIC_DIRECTORY = "C:\\Users\\Max\\Desktop\\music\\small"
    music_files = get_songs(music_dir=MUSIC_DIRECTORY)

    for i, song_path in enumerate(music_files):
        print(f"{i+1}. {song_path.stem}")
        synced, unsynced =  fetch_lyrics(song_path=song_path)
        with open(f"lyrics/{song_path.stem}.lrc", "w", encoding="utf-8") as f:
            f.write(f"{song_path.stem}\nsynced\n\n{synced}")
            f.write(f"\n{song_path.stem}\nunsynced\n\n{unsynced}")











