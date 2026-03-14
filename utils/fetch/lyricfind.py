import requests
import json
from utils.helpers import build_search_query, match_song_metadata
from utils.fetch.musixmatch import DRIVER


def fetch_lyrics(song_path: str) -> tuple:
    search_query = build_search_query(song_path=song_path)

    limit = 10
    req_url = f"https://lyrics.lyricfind.com/api/v1/search?reqtype=default&territory=IN&searchtype=track&all={search_query}&alltracks=no&limit={limit}&output=json&useragent=Mozilla%2F5.0+(Windows+NT+10.0%3B+Win64%3B+x64)+AppleWebKit%2F537.36+(KHTML,+like+Gecko)+Chrome%2F144.0.0.0+Safari%2F537.36"

    res = requests.get(req_url)

    res.raise_for_status()

    # print(res.text)

    with open("lyrics/lyricfind.json", mode="w", encoding="utf-8") as f:
        json.dump(res.json(), f, ensure_ascii=False, indent=2)

    print("Done - lyricfind")

    data = res.json()
    status = data.get("response", "").get("description", "")
    if (status != "SUCCESS"):
        return False, False
    
    tracks:list = data.get("tracks", [])
    
    for track_item in tracks:
        recieved_song_description = ""

        recieved_song_title:str = track_item.get("title", "")
        recieved_song_description += recieved_song_title

        artists:list = track_item.get("artists", [])
        for artist in artists:
            recieved_song_description += " " + artist.get("name", "")
        
        flag_match = match_song_metadata (threshold=70, print_match=True, local_song_path=song_path, received_song_info=recieved_song_description)
        # print(flag_match)
        if not flag_match: continue

        lyricfind_url = track_item.get("lyricfind_url", "")
        print(lyricfind_url)

        DRIVER.get(url=lyricfind_url)
        import time
        time.sleep(600)

        
        



if __name__ == "__main__":
    MUSIC_DIRECTORY = "C:\\Users\\Max\\Desktop\\music\\small\\Arijit Singh - Zara Si Dosti.flac"
    fetch_lyrics(song_path=MUSIC_DIRECTORY)






