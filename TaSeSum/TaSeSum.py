import reflex as rx
from TaSeSum.components.upload import Uploader, UploaderState
from TaSeSum.components.summary_card import SummaryCard, render_summary_card

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


class State(UploaderState):
    viz_ready: bool = False
    segments: list[list[dict]]

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

        async with self:
            self.viz_ready = True


@rx.page(on_load=State.load)
def index() -> rx.Component:
    return rx.flex(
        Uploader(),
        rx.cond(
            State.video_path,
            rx.button("Process", type="submit", on_click=State.process_video),
        ),
        rx.cond(
            State.viz_ready,
            rx.foreach(State.segments, render_summary_card)
        ),
        align="center",
        justify="center",
        direction="column",
        margin=20,
        gap=20,
    )


app = rx.App()
app.add_page(index)
