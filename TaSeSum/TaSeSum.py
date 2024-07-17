import reflex as rx
from TaSeSum.components.upload import UploadComponent, UploadState

from src.audio_utils import extract_audio_from_video
from src.transcription import (
    load_stable_whisper_model,
    merge_segments_primary,
    merge_segments_secondary,
)
from src.topic_modelling import (
    load_topic_model,
    add_topic_to_segments,
)


class State(UploadState):
    async def load(self):
        self.transcription_model = load_stable_whisper_model("tiny")
        self.topic_model = load_topic_model()

    @rx.background
    async def process_video(self):
        # Transcription
        audio_path = extract_audio_from_video(self.video_path)
        result = self.transcription_model.transcribe(audio_path, word_timestamps=True)
        result_dict = result.to_dict()

        # Segment merging
        segments = merge_segments_primary(result_dict["segments"])
        segments_with_topic = add_topic_to_segments(segments, self.topic_model)
        segments = merge_segments_secondary(segments_with_topic)


@rx.page(on_load=State.load)
def index() -> rx.Component:
    return rx.flex(
        UploadComponent(),
        rx.cond(
            State.video_path,
            rx.button("Process", type="submit", on_click=State.process_video),
        ),
        align="center",
        justify="center",
        direction="column",
        margin=20,
        gap=20,
    )


app = rx.App()
app.add_page(index)
