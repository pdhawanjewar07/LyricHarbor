import requests
from utils.config import SPOTIFY_TRACK_CSS_SELECTOR
from utils.helpers import extract_spotify_lyrics
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from syrics.api import Spotify
from utils.selenium_startup import get_driver
from dotenv import load_dotenv
import os

load_dotenv()
SPOTIFY_DC_TOKEN = os.getenv("SPOTIFY_DC_TOKEN")

sp = Spotify(SPOTIFY_DC_TOKEN)

driver = get_driver()

def lyrics_musixmatch_via_spotify(search_query: str, mode:int) -> str|bool:
    """
    Fetch lyrics json response from musixmatch_via_spotify
    
    Args:
        search_query: clean search query.
        mode: synced(0), unsynced(1), synced_with_fallback(2)

    Returns:
        Lyrics(str) if found, otherwise False
    """
    url = f"https://open.spotify.com/search/{requests.utils.quote(search_query)}/tracks"

    try:
        driver.get(url)
        first_track = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, SPOTIFY_TRACK_CSS_SELECTOR)))
    except: 
        # print("Lyrics not found - MusixMatch")
        return False

    old_url = driver.current_url
    first_track.click()
    WebDriverWait(driver, 30).until(lambda d: d.current_url != old_url and "/track/" in d.current_url)

    track_url = driver.current_url
    print(track_url)
    match = re.search(r"/track/([A-Za-z0-9]+)", track_url)
    track_id = match.group(1)
    # print(track_id)

    json_response = sp.get_lyrics(track_id=track_id)
    # print(json_response)
    lyrics = extract_spotify_lyrics(json_data=json_response, mode=mode)
    try:
        return lyrics
    except:
        return False


"""
query_list = ["Chokra Jawaan"] # ,"Bezubaan Phir Se ABCD 2","Jaane Bhi De Heyy Babyy","Ha Raham Mehfuz"
for index, query in enumerate(query_list):
    print(f"starting - {index}")
    lyrics = lyrics_musixmatch_via_spotify(search_query=query)

    if lyrics:
        with open(f"lyrics/{query}.lrc", "w", encoding="utf-8") as f:
            f.write(lyrics)
        print("SUCCESS - Lyrics found")
    else: print("FAILURE - No lyrics found")

"""