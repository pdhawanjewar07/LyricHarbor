import requests
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from syrics.api import Spotify
from utils.config import SPOTIFY_TRACK_CSS_SELECTOR
from utils.helpers import extract_spotify_lyrics, build_search_query
from utils.selenium_startup import get_driver
from dotenv import load_dotenv
import os
import logging


load_dotenv()
SPOTIFY_DC_TOKEN = os.getenv("SPOTIFY_DC_TOKEN")

log = logging.getLogger(__name__)
sp = Spotify(SPOTIFY_DC_TOKEN)
driver = get_driver()

def fetch_lyrics(song_path: str, mode:int) -> str|bool:
    """
    Fetch lyrics json response from musixmatch_via_spotify
    
    Args:
        search_query: song path
        mode: synced(0), unsynced(1), synced_with_fallback(2)

    Returns:
        Lyrics(str) if found, otherwise False
    """

    search_query = build_search_query(song_path=song_path, source=0)

    url = f"https://open.spotify.com/search/{requests.utils.quote(search_query)}/tracks"

    try:
        driver.get(url)
        first_track = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, SPOTIFY_TRACK_CSS_SELECTOR)))
    except: 
        log.info("Spotify: could not get track(selenium driver time out)")
        return False

    old_url = driver.current_url
    first_track.click()
    WebDriverWait(driver, 30).until(lambda d: d.current_url != old_url and "/track/" in d.current_url)

    track_url = driver.current_url
    # print(track_url)
    match = re.search(r"/track/([A-Za-z0-9]+)", track_url)
    track_id = match.group(1)
    # print(track_id)

    json_response = sp.get_lyrics(track_id=track_id)
    # print(json_response)
    lyrics = extract_spotify_lyrics(json_data=json_response, mode=mode)
    if lyrics:
        log.info("SUCCESS - MusixMatch: lyrics found")
        return lyrics
    
    log.info("FAILURE - MusixMatch: lyrics not found")
    return False

if __name__ == "__main__":
    lyrics = fetch_lyrics(song_path="C:\\Users\\Max\\Desktop\\music\\small\\Outstation - Tum Se.flac", mode=0)
    # print(lyrics)