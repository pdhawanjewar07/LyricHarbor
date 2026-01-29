from utils import config
from pathlib import Path
import os

def main(music_directory:str) -> int:
    """
    main function

    Args:
        music_directory: directory containing music

    Returns:
        0
    """

    music_directory = Path(music_directory)

    music_files = [f for f in music_directory.iterdir() if f.is_file() and f.suffix.lower() in config.AUDIO_EXTENSIONS]
    for name in music_files:
        print(name)
    return 0

main(music_directory=config.music_directory)

