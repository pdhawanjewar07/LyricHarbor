from pathlib import Path
import shutil


def move_flac_lrc_pairs(src_dir: str, dst_dir: str) -> None:
    src = Path(src_dir)
    dst = Path(dst_dir)

    if not src.is_dir():
        raise ValueError(f"Source directory does not exist: {src}")

    dst.mkdir(parents=True, exist_ok=True)

    flac_files = src.glob("*.flac")

    for flac in flac_files:
        lrc = flac.with_suffix(".lrc")

        if lrc.exists():
            shutil.move(str(flac), dst / flac.name)
            shutil.move(str(lrc), dst / lrc.name)


if __name__ == "__main__":
    SOURCE_DIR = r"C:\\Users\\Max\\Desktop\\music"
    DEST_DIR = r"C:\\Users\\Max\\Desktop\\music\\found"

    move_flac_lrc_pairs(SOURCE_DIR, DEST_DIR)