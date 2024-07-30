import os
import yt_dlp

UPLOADS_FOLDER = f"{os.getcwd()}/uploaded_files"


def download_video(url: str) -> str:
    ext = "mp4"
    output_template = f"{UPLOADS_FOLDER}/%(id)s.{ext}"
    cfg = {
        "format": "bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/mp4",
        "outtmpl": f"{output_template}",
    }
    try:
        with yt_dlp.YoutubeDL(cfg) as video:
            info_dict = video.extract_info(url, download=True)
            video_id = info_dict["id"]
    except Exception as e:
        return None

    output_path = f"{UPLOADS_FOLDER}/{video_id}.{ext}"
    return output_path
