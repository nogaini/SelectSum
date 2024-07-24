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
        trim_path = trim_video(self.video_path, segment["start"], segment["end"])

        async with self:
            self.data_dict[segment_idx] = {}
            self.data_dict[segment_idx]["trimmed_video_path"] = trim_path

        res = summarizer.summarize(segment["text"])
        async with self:
            self.data_dict[segment_idx]["title"] = res.title
            self.data_dict[segment_idx]["summary"] = res.summary
            self.data_dict[segment_idx]["bullets"] = res.bullets


def render_summary_card(segment: Segment) -> rx.Component:
    segment_idx = segment.idx
    return rx.card(
        rx.flex(
            rx.inset(
                rx.image(rx.get_upload_url(segment.wordcloud_img_path)),
                width="640px",
                height="auto",
                side="top",
                pb="current",
            ),
            rx.flex(
                status_chip(segment.topic_tags, "info", "blue"),
                justify="center",
            ),
            rx.button(
                "Summarize",
                on_click=SummaryCardState.generate_summary(segment),
            ),
            rx.cond(
                SummaryCardState.data_dict[segment_idx],
                rx.cond(
                    SummaryCardState.data_dict[segment_idx].trimmed_video_path,
                    rx.inset(
                        rx.video(
                            url=rx.get_upload_url(
                                SummaryCardState.data_dict[
                                    segment_idx
                                ].trimmed_video_path
                            ),
                            width="640px",
                            height="auto",
                        ),
                    ),
                ),
            ),
            rx.cond(
                SummaryCardState.data_dict[segment_idx],
                rx.cond(
                    SummaryCardState.data_dict[segment_idx].title,
                    rx.flex(
                        rx.text(
                            SummaryCardState.data_dict[segment_idx].title,
                            size="7",
                            align="center",
                        ),
                        rx.flex(
                            rx.foreach(
                                SummaryCardState.data_dict[segment_idx].bullets,
                                rx.list.item,
                            ),
                            direction="column",
                        ),
                        direction="column",
                        gap=10,
                        align="center",
                    ),
                ),
            ),
            direction="column",
            gap=30,
        ),
        width="640px",
        border="1px solid #00ff44",
    )
