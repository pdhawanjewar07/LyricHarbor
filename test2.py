import requests
import json


query = "Zara+Si+Dosti"
limit = 10

req_url = f"https://lyrics.lyricfind.com/api/v1/search?reqtype=default&territory=IN&searchtype=track&all={query}&alltracks=no&limit={limit}&output=json&useragent=Mozilla%2F5.0+(Windows+NT+10.0%3B+Win64%3B+x64)+AppleWebKit%2F537.36+(KHTML,+like+Gecko)+Chrome%2F144.0.0.0+Safari%2F537.36"

res = requests.get(req_url)

res.raise_for_status()

# print(res.text)

with open("lyrics/lyricfind.json", mode="w", encoding="utf-8") as f:
    json.dump(res.json(), f, ensure_ascii=False, indent=2)






