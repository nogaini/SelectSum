import reflex as rx
from TaSeSum.components.upload import Uploader, UploaderState
from TaSeSum.components.summary_card import render_summary_card
from TaSeSum.components.topic_chips import TopicChipsSelector, TopicChipsState
from TaSeSum.state import CommonState

from src.text_utils import WordCloudGenerator
from src.audio_utils import extract_audio_from_video
from src.transcription import load_stable_whisper_model
from src.segment_utils import (
    merge_segments_primary,
    merge_segments_secondary,
    add_wordcloud_to_segments,
)
from src.topic_modelling import (
    load_topic_model,
    add_topic_to_segments,
)


class IndexState(CommonState):
    segments: list[dict]
    topic_dict: dict[int, list[str]] = None

    async def load(self):
        self.transcription_model = load_stable_whisper_model("tiny")
        self.topic_model = load_topic_model()
        self.wc_generator = WordCloudGenerator()

    @rx.background
    async def process_video(self):
        # Transcription
        audio_path = extract_audio_from_video(str(self.video_path))
        result = self.transcription_model.transcribe(audio_path, word_timestamps=True)
        result_dict = result.to_dict()
        segments = result_dict["segments"]

        # Segment merging
        segments = merge_segments_primary(segments)

        segments_with_topic, topic_dict, all_topic_tags = add_topic_to_segments(
            segments, self.topic_model
        )
        segments = merge_segments_secondary(segments_with_topic)
        segments = add_wordcloud_to_segments(segments, self.wc_generator)

        async with self:
            self.segments = segments
            self.selected_items = all_topic_tags


@rx.page(on_load=IndexState.load)
def index() -> rx.Component:
    return rx.flex(
        Uploader(),
        rx.cond(
            IndexState.video_path,
            rx.button("Process", type="submit", on_click=IndexState.process_video),
        ),
        rx.cond(IndexState.selected_items, TopicChipsSelector()),
        rx.cond(
            IndexState.selected_items,
            rx.foreach(IndexState.segments, render_summary_card),
        ),
        align="center",
        justify="center",
        direction="column",
        margin=20,
        gap=20,
    )


app = rx.App()
app.add_page(index)
