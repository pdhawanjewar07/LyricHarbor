from utils import config, build, clean, fetch, extract_save
from pathlib import Path
import os

def main(music_dir:str, out_dir:str) -> int:
    """
    main function

    Args:
        music_dir: music source directory
        out_dir: output directory for lyrics

    Returns:
        0
    """
    total_processed = 0
    total_found_and_saved = 0

    music_dir = Path(music_dir)
    music_files = [f for f in music_dir.iterdir() if f.is_file() and f.suffix.lower() in config.AUDIO_EXTENSIONS]
    for song in music_files:
        # print(song.stem)
        # """
        total_processed += 1
        print(f"{total_processed}. {song.stem}")

        # build raw search query
        query = build.raw_search_query(song_path=str(song), tags_to_include=['title', 'artist', 'album'])

        # clean query
        query = clean.search_query(query=query)
        print(f"Query: {query}")

        # fetch lyrics as json response
        json_lyrics_data = fetch.lyrics(search_query=query)

        # extract and save lyrics to location
        if extract_save.lyrics(json_data=json_lyrics_data, out_dir=out_dir, out_filename=song.stem, mode=1):
            total_found_and_saved += 1
            print("SUCCESS - found")
        else: print("FAILED - not found")

    print(f"\nSuccess Rate: {(total_found_and_saved/total_processed)*100}% | {total_found_and_saved}/{total_processed}")
    # """
    return 0


main(music_dir=config.MUSIC_DIRECTORY, out_dir=config.OUTPUT_DIRECTORY)

