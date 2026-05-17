import logging
from pathlib import Path
from pathlib import Path

from moviepy.editor import VideoFileClip

from config import (
    VIDEOS_DIR,
    CHUNKS_DIR,
    VIDEO_PADDING
)

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


def chunk_video(
        document_name,
        start_time,
        end_time,
        directory=VIDEOS_DIR
):

    video_path = Path(directory) / document_name

    output_dir = Path(CHUNKS_DIR)

    output_dir.mkdir(exist_ok=True)

    clip_name = (
        f"{document_name}_"
        f"{int(start_time)}_"
        f"{int(end_time)}.mp4"
    )

    output_path = output_dir / clip_name

    with VideoFileClip(str(video_path)) as video:

        duration = video.duration

        padding = VIDEO_PADDING

        start_time = max(
            0,
            start_time - padding
        )

        end_time = min(
            duration,
            end_time + padding
        )

        clip = video.subclip(
            start_time,
            end_time
        )

        clip.write_videofile(
            str(output_path),
            codec="libx264",
            audio_codec="aac",
            logger=None
        )

    logger.info(
        f"Clip saved: {output_path}"
    )

    return output_path