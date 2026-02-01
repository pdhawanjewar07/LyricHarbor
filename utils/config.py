# preferences
LYRICS_SOURCES = ["musixmatch-via-spotify", "lrclib", "lyricsfind-via-ytmusic" "genius"] # order matters(by priority)
AUDIO_EXTENSIONS = {".mp3", ".flac", ".wav", ".aac", ".m4a",".ogg", ".opus", ".alac", ".aiff"}

# music paths
MUSIC_DIRECTORY = "C:/Users/Max/Desktop/music/small" # non recursive musixmatch_found
OUTPUT_DIRECTORY = "C:/Users/Max/Desktop/music/small"

# chrome & driver paths
DRIVER_PATH = "C:/Users/Max/Desktop/VS-Code/Github Repositories/time-synced-lyrics/bin/chromedriver-win64/chromedriver.exe"  # must correspond to chrome version
CHROME_BINARY = r"C:/Users/Max/Desktop/VS-Code/Github Repositories/time-synced-lyrics/bin/chrome-win64/chrome.exe"

# tokens
# SPOTIFY_DC_TOKEN = "AQDGsY5iVkiaKcJhE0l06cmnLiU33bfo-5V-6b3bpchEbfR9zEGHoABUrAgk5uRaGDnmSqhbnQcHjqWxZhP5rreESso86KAfozICZLqwC__Th5Rzv2GeOmjYFHrGIjXJnQ5fio5k5v9PSbc50hi1DEDxlG8zkc5yYOBjge3ZVWCPOVUYGVdArVZjXWGr2K63QG_J_dFItZyPW-_OPB0"
# GENIUS_AUTH_BEARER_TOKEN = "zWg_WY0oZeuYA_0JxsNZwJ4F34jMe66zRZhJh1OAIZ1qO2O7gF6Q6qx5GxyjltIR"

# selenium element identifiers
SPOTIFY_TRACK_CSS_SELECTOR = "#searchPage > div > div > div > div.eaxF79s4oV8I2CPQ > div > div.m9t_KhZ6MI0XQj9b > div:nth-child(2) > div:nth-child(1) > div > div.NILrlF6tOUcbSyzo > div > a > div"
GENIUS_LYRICS_ELEMENT_XPATH = '//*[@id="lyrics-root"]/div[1]'

