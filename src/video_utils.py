import ffmpeg
import cv2
import os
import numpy as np
from src.text_utils import generate_random_string

TRIMS_FOLDER = f"{os.getcwd()}/uploaded_files/trims"
RX_TRIMS_FOLDER = "trims"

KEYFRAMES_FOLDER = f"{os.getcwd()}/uploaded_files/keyframes"
RX_KEYFRAMES_FOLDER = "keyframes"


def get_video_duration(video_path: str):
    probe = ffmpeg.probe(video_path)
    duration = float(probe["format"]["duration"])
    return duration


def write_keyframe(frame: np.array) -> str:
    os.makedirs(KEYFRAMES_FOLDER, exist_ok=True)
    filename = generate_random_string(10)
    kf_path = f"{KEYFRAMES_FOLDER}/{filename}.jpg"
    cv2.imwrite(kf_path, frame)
    return f"{RX_KEYFRAMES_FOLDER}/{filename}.jpg"


def trim_video(
    video_path: str, start_time: float, end_time: float, offset: float = 0.0
) -> str:
    os.makedirs(TRIMS_FOLDER, exist_ok=True)
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


class VideoReader:
    def __init__(self, video_path: str):
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"{video_path} not found!")

        self._video_path = video_path
        self._vr = cv2.VideoCapture()
        self._vr.open(video_path)

        res, frame = self.read()
        if res:
            self.frame_channels = int(frame.shape[-1])
        else:
            raise IOError(f"Cannot read frame from {video_path}!")
        self._seek(0)

    def __del__(self):
        try:
            self._vr.release()
        except AttributeError:
            pass

    def __len__(self):
        return self.number_of_frames

    def __getitem__(self, index):
        if isinstance(index, slice):
            return (self[ii] for ii in range(*index.indices(len(self))))
        elif isinstance(index, (list, tuple, range)):
            return (self[ii] for ii in index)
        else:
            return self.read(index)[1]

    def __repr__(self):
        return f"{self._video_path} with {len(self)} frames of size {self.frame_shape} at {self.fps:1.2f} fps"

    def __iter__(self):
        return self[:]

    def __enter__(self):
        return self

    def __exit__(self):
        del self

    def read(self, idx: int = None):
        is_current_frame = idx == self.current_frame_pos
        if idx is not None and not is_current_frame:
            self._seek(idx)
        ret, frame = self._vr.read()
        return ret, frame

    def close(self):
        self._vr.release()

    def _reset(self):
        self.__init__(self._video_path)

    def _seek(self, idx: int):
        self._vr.set(cv2.CAP_PROP_POS_FRAMES, idx)

    @property
    def current_frame_pos(self):
        return self._vr.get(cv2.CAP_PROP_POS_FRAMES)

    @property
    def number_of_frames(self):
        return int(self._vr.get(cv2.CAP_PROP_FRAME_COUNT))

    @property
    def fps(self):
        return round(self._vr.get(cv2.CAP_PROP_FPS))

    @property
    def frame_width(self):
        return int(self._vr.get(cv2.CAP_PROP_FRAME_WIDTH))

    @property
    def frame_height(self):
        return int(self._vr.get(cv2.CAP_PROP_FRAME_HEIGHT))

    @property
    def fourcc(self):
        return int(self._vr.get(cv2.CAP_PROP_FOURCC))

    @property
    def frame_format(self):
        return int(self._vr.get(cv2.CAP_PROP_FORMAT))

    @property
    def frame_shape(self):
        return (self.frame_height, self.frame_width, self.frame_channels)
