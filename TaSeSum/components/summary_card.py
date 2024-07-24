import reflex as rx
from TaSeSum.components.topic_chips import status_chip
from TaSeSum.components.upload import UploaderState
from src.summarization import Summarizer
from src.video_utils import trim_video


class Segment(rx.Base):
    text: str
    start: float
    end: float
    topic_id: int
    topic_tags: str
    idx: int
    wordcloud_img_path: str


class InnerFields(rx.Base):
    title: str = ""
    summary: str = ""
    bullets: list[str] = []
    trimmed_video_path: str = ""


class SummaryCardState(UploaderState):
    data_dict: dict[int, InnerFields]

    @rx.background
    async def generate_summary(self, segment: Segment):
        summarizer = Summarizer()

        segment_idx = segment["idx"]
        res = summarizer.summarize(segment["text"])
        trim_path = trim_video(self.video_path, segment["start"], segment["end"])

        async with self:
            self.data_dict[segment_idx] = {}
            self.data_dict[segment_idx]["title"] = res.title
            self.data_dict[segment_idx]["summary"] = res.summary
            self.data_dict[segment_idx]["bullets"] = res.bullets
            self.data_dict[segment_idx]["trimmed_video_path"] = trim_path


def render_summary_card(segment: Segment) -> rx.Component:
    segment_idx = segment.idx
    return rx.card(
        rx.flex(
            rx.inset(
                rx.image(rx.get_upload_url(segment.wordcloud_img_path)),
                side="top",
                pb="current",
            ),
            rx.text("Topics"),
            status_chip(segment.topic_tags, "info", "blue"),
            rx.divider(),
            rx.button(
                "Summarize",
                on_click=SummaryCardState.generate_summary(segment),
            ),
            rx.cond(
                SummaryCardState.data_dict[segment_idx],
                rx.video(
                    url=rx.get_upload_url(
                        SummaryCardState.data_dict[segment_idx].trimmed_video_path
                    )
                ),
            ),
            rx.divider(),
            rx.cond(
                SummaryCardState.data_dict[segment_idx],
                rx.flex(
                    rx.text(SummaryCardState.data_dict[segment_idx].title),
                    rx.foreach(
                        SummaryCardState.data_dict[segment_idx].bullets, rx.text
                    ),
                    direction="column",
                ),
            ),
            direction="column",
        ),
    )
