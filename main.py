from utils.helpers import save_lyrics, format_time
from config import MUSIC_DIRECTORY, OUTPUT_DIRECTORY, LYRICS_FETCH_MODE
from utils.playwright_clear_cache import clear_playwright_cache
from pathlib import Path
import logging
from utils.fetch.from_all import fetch_lyrics
import time

def main() -> int:
    """main function

    :return: 0
    :rtype: int
    """
    start_time = time.time()
    log = logging.getLogger(__name__)

    total_processed = 0
    total_found_and_saved = 0

    AUDIO_EXTENSIONS = {".mp3", ".flac", ".wav", ".aac", ".m4a",".ogg", ".opus", ".alac", ".aiff"}
    music_dir = Path(MUSIC_DIRECTORY)
    music_files = (
        f for f in music_dir.iterdir()
        if f.is_file() and f.suffix.lower() in AUDIO_EXTENSIONS
    )

    for song_path in music_files:
        total_processed += 1
        try:
            log.info(f"{total_processed}. {song_path.stem}")
            lyrics = fetch_lyrics(song_path=song_path, fetch_mode=LYRICS_FETCH_MODE)
            if isinstance(lyrics, str):
                # save lyrics to location
                save_lyrics(lyrics=lyrics, out_dir=OUTPUT_DIRECTORY, out_filename=song_path.stem) # song.stem = song filename only
                total_found_and_saved += 1

        except Exception as e: log.exception(f"FAILED: {song_path.name}")

    clear_playwright_cache()

    success_rate = (total_found_and_saved / total_processed) * 100 if total_processed else 0.0
    end_time = time.time() - start_time
    avg_time_per_song_found = end_time / total_found_and_saved
    log.info("==== Summary ====")
    log.info(f"Success Rate: {success_rate:0.2f}% | {total_found_and_saved}/{total_processed}")
    log.info(f"Average time per song found: {avg_time_per_song_found:0.2f}(seconds)")
    log.info(f"Total elapsed time: {format_time(end_time)}") # 23hrs:12min:59sec,213ms
    return 0

if __name__ == "__main__":
    main()

