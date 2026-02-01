import requests
from utils.config import GENIUS_LYRICS_ELEMENT_XPATH
from utils.helpers import extract_genius_song_url
from utils.selenium_startup import get_driver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from dotenv import load_dotenv
import os

load_dotenv()
GENIUS_AUTH_BEARER_TOKEN = os.getenv("GENIUS_AUTH_BEARER_TOKEN")

driver = get_driver()

def lyrics_genius(search_query: str) -> str | bool:
    url = "https://api.genius.com/search"
    headers = {"Authorization": f"Bearer {GENIUS_AUTH_BEARER_TOKEN}"}
    params = {"q": search_query}

    resp = requests.get(url, headers=headers, params=params, timeout=10)
    if resp.status_code != 200: return False
    json_response = resp.json()
    # get genius song url
    song_url = extract_genius_song_url(json_data=json_response)
    if song_url is False: return False

    print(song_url)
    print("visiting url")
    st = time.time()
    driver.get(song_url)
    elapsed = time.time() - st
    print(f"url visited({elapsed:0.2f}s)")
    print("waiting to find lyrics element")
    st = time.time()
    lyrics_element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, GENIUS_LYRICS_ELEMENT_XPATH)))
    elapsed = time.time() - st
    print(f"element found({elapsed:0.2f}s)")

    # print(lyrics_element.text)
    return lyrics_element.text


# sawaal abhijeet srivastava (1), urzu urzu durkut (0), aazmale aazmale (1)
# lyrics_genius(search_query="sawaal abhijeet srivastava")


