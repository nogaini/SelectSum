import ffmpeg

AUDIO_FOLDER = "/home/jobin/Projects/TaSeSum/uploaded_files/audio"


def extract_audio_from_video(video_path: str) -> str:
    filename = video_path.split("/")[-1].split(".")[0]
    audio_path = f"{AUDIO_FOLDER}/{filename}.wav"
    (
        ffmpeg.input(video_path)
        .output(audio_path, **{"q:a": 0, "map": "a"})
        .run(overwrite_output=True)
    )
    return audio_path
