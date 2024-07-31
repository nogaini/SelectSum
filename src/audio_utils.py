import os
import ffmpeg

AUDIO_FOLDER = f"{os.getcwd()}/uploaded_files/audio"


def extract_audio_from_video(video_path: str) -> str:
    os.makedirs(AUDIO_FOLDER, exist_ok=True)
    filename = video_path.split("/")[-1].split(".")[0]
    audio_path = f"{AUDIO_FOLDER}/{filename}.wav"
    (
        ffmpeg.input(video_path)
        .output(audio_path, **{"q:a": 0, "map": "a"}, loglevel="quiet")
        .run(overwrite_output=True)
    )
    return audio_path
