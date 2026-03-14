import requests
from utils.spotify_auth import SpotifyAuthManager

auth = SpotifyAuthManager()
SPOTIFY_AUTH_TOKEN = auth.get_token()
print(SPOTIFY_AUTH_TOKEN)

def search_spotify(query, token, limit=10):
    url = "https://api.spotify.com/v1/search"
    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
    }
    params = {
        "q": query,          # Example: "track:Believer artist:Imagine Dragons album:Evolve"
        "type": "track",     # Example: "track:o re kanchi artist:anu malik album:asoka (original motion picture soundtrack)"
        "limit": limit
    }

    response = requests.get(url, headers=headers, params=params, timeout=3)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    token = SPOTIFY_AUTH_TOKEN

    # You can combine filters like this:
    query = "track:ajnabi shehar artist:sonu nigam"

    results = search_spotify(query, token, limit=1)

    print(results)  # Full JSON response

