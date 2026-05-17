from pathlib import Path
import yt_dlp

from config import VIDEOS_DIR


def download_youtube_video(url):

    output_dir = Path(VIDEOS_DIR)

    output_dir.mkdir(exist_ok=True)

    ydl_opts = {
        "outtmpl": str(
            output_dir / "%(title)s.%(ext)s"
        ),
        "format": "mp4"
    }

    with yt_dlp.YoutubeDL(
        ydl_opts
    ) as ydl:

        info = ydl.extract_info(
            url,
            download=True
        )

        filename = ydl.prepare_filename(info)

    return filename