from typing import Optional

import reflex as rx
from TaSeSum.components.upload import Uploader
from TaSeSum.components.download import Downloader

from TaSeSum.components.summary_card import render_summary_card, SummaryCardState
from TaSeSum.components.topic_chips import TopicChipsSelector
from TaSeSum.state import CommonState

from src.text_utils import WordCloudGenerator
from src.audio_utils import extract_audio_from_video
from src.video_utils import VideoReader
from src.transcription import load_stable_whisper_model
from src.segment_utils import (
    merge_segments_primary,
    merge_segments_secondary,
    add_wordcloud_to_segments,
    add_idx_to_segments,
    add_keyframes_to_segments,
)
from src.topic_modelling import add_topic_to_segments


def custom_backend_handler(
    exception: Exception,
) -> Optional[rx.event.EventSpec]:
    if isinstance(exception, ValueError):
        return rx.toast.error(
            "Video is either too short or is not transcript-heavy. Please refresh and try another video."
        )


class IndexState(CommonState):
    progress_value: int = 0

    async def load(self):
        (await self.get_state(rx.State)).reset()
        self.transcription_model = load_stable_whisper_model("tiny")
        self.wc_generator = WordCloudGenerator()

    @rx.background
    async def process_video(self):
        # Init
        async with self:
            (await self.get_state(SummaryCardState)).reset()
            self.selected_items = []
            self.segments = []
            self.segments_in_view = []
            self.all_items = []
            self.process_button_is_disabled = True

            self.progress_value = 50
            self.process_text = "Transcribing..."

        vr = VideoReader(str(self.video_path))
        video_fps = vr.fps

        # Transcription
        audio_path = extract_audio_from_video(str(self.video_path))
        result = self.transcription_model.transcribe(audio_path, word_timestamps=False)
        async with self:
            self.progress_value = 80
            self.process_text = "Identifying topics..."

        result_dict = result.to_dict()
        segments = result_dict["segments"]

        # Primary segment merging
        segments = merge_segments_primary(segments)

        # Add topic tags
        segments_with_topic, all_topic_tags = add_topic_to_segments(segments)

        async with self:
            self.progress_value = 90
            self.process_text = "Generating wordclouds..."

        # Secondary segment merging
        segments = merge_segments_secondary(segments_with_topic)
        segments = add_idx_to_segments(segments)

        # Generate wordclouds
        segments = add_wordcloud_to_segments(segments, self.wc_generator)

        async with self:
            self.progress_value = 95
            self.process_text = "Extracting keyframes..."

        # Extract keyframes
        segments = add_keyframes_to_segments(segments, video_fps, vr)

        async with self:
            self.progress_value = 100

        async with self:
            self.process_text = ""
            self.progress_value = 0
            self.segments = segments
            self.segments_in_view = segments
            self.selected_items = all_topic_tags
            self.all_items = all_topic_tags


@rx.page(on_load=IndexState.load, title="SelectSum")
def index() -> rx.Component:
    return rx.flex(
        rx.text(
            rx.text.strong("SelectSum"),
            ": Topic-based ",
            rx.text.strong("Select"),
            "ive ",
            rx.text.strong("Sum"),
            "marization of speech-based videos",
            size="9",
            align="center",
        ),
        rx.text(
            "Select a local file or fetch an online video.",
            size="5",
        ),
        Downloader(),
        Uploader(),
        rx.cond(
            IndexState.video_path,
            rx.button(
                "Process",
                type="submit",
                align="center",
                disabled=IndexState.process_button_is_disabled,
                on_click=IndexState.process_video,
            ),
        ),
        rx.cond(
            IndexState.progress_value,
            rx.progress(value=IndexState.progress_value, max=100),
        ),
        rx.cond(
            IndexState.process_text,
            rx.flex(
                rx.spinner(size="3"),
                rx.text(IndexState.process_text),
                align="center",
                justify="center",
                gap=5,
            ),
        ),
        rx.flex(
            rx.cond(IndexState.segments, TopicChipsSelector()),
            rx.cond(
                IndexState.selected_items,
                rx.flex(
                    rx.foreach(IndexState.segments_in_view, render_summary_card),
                    gap=50,
                    align="start",
                    justify="center",
                    wrap="wrap",
                ),
            ),
            gap=150,
            direction="column",
            align="center",
            justify="center",
            margin=20,
        ),
        align="center",
        justify="center",
        direction="column",
        margin=50,
        gap=20,
    )


app = rx.App(backend_exception_handler=custom_backend_handler)
app.add_page(index)
