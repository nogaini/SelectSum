import ffmpeg
import os
from src.text_utils import generate_random_string

TRIMS_FOLDER = f"{os.getcwd()}/uploaded_files/trims"
RX_TRIMS_FOLDER = "trims"


def get_video_duration(video_path: str):
    probe = ffmpeg.probe(video_path)
    duration = float(probe["format"]["duration"])
    return duration


def trim_video(
    video_path: str, start_time: float, end_time: float, offset: float = 0.0
) -> str:
    filename = str(video_path).split("/")[-1].split(".")[0]
    suffix = generate_random_string(10)
    trim_path = f"{TRIMS_FOLDER}/{filename}_{suffix}.mp4"

    duration = get_video_duration(video_path)

    (
        ffmpeg.input(
            video_path,
            ss=max(start_time - offset, 0.0),
            to=min(end_time + offset, duration),
        )
        .output(
            trim_path,
            vcodec="libx264",
            acodec="aac",
            strict="experimental",
        )
        .global_args("-loglevel", "error")
        .run(overwrite_output=True)
    )
    return f"{RX_TRIMS_FOLDER}/{filename}_{suffix}.mp4"
