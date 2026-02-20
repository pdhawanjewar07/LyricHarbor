# import requests
from syrics.api import Spotify
import json
from dotenv import load_dotenv
import os
# from utils.totp import TOTP

load_dotenv()

sp_dc = os.getenv("SP_DC_TOKEN")



TRACK_ID = "0dfDtMJigXYVWoqNovKPA3" 
# SP_DC = "your_sp_dc_cookie_here"
OUTPUT_FILE = "synced_lyrics.json"

def save_synced_lyrics(track_id):
    sp = Spotify(sp_dc)

    lyrics_data = sp.get_lyrics(track_id)

    if not lyrics_data or "lyrics" not in lyrics_data:
        print("No synced lyrics found.")
        return

    synced_lines = lyrics_data["lyrics"]["lines"]

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(synced_lines, f, indent=4, ensure_ascii=False)

    print("Saved synced lyrics.")

if __name__ == "__main__":
    save_synced_lyrics(TRACK_ID)
