import reflex as rx
from TaSeSum.components.topic_chips import status_chip
from TaSeSum.state import CommonState
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
    idx_keyframe_pairs: list[list[int, str]]


class SummaryFields(rx.Base):
    title: str = ""
    summary: str = ""
    bullets: list[str] = []
    trimmed_video_path: str = ""
    summary_process_text: str = ""
    display_img: str = ""


class SummaryCardState(CommonState):
    summary_dicts: dict[int, SummaryFields]
    clicked_keyframe: bool = False

    def set_display_image(self, segment_idx: int, kf_path: str):
        self.summary_dicts[segment_idx]["display_img"] = kf_path
        self.clicked_keyframe = True

    @rx.background
    async def generate_summary(self, segment: Segment):
        segment_idx = segment["idx"]
        async with self:
            self.summary_dicts[segment_idx] = {}
            self.summary_dicts[segment_idx]["summary_process_text"] = (
                "Trimming video..."
            )

        summarizer = Summarizer()
        trim_path = trim_video(self.video_path, segment["start"], segment["end"])

        async with self:
            self.summary_dicts[segment_idx]["trimmed_video_path"] = trim_path
            self.summary_dicts[segment_idx]["summary_process_text"] = (
                "Generating summary..."
            )

        res = summarizer.summarize(segment["text"])
        async with self:
            self.summary_dicts[segment_idx]["title"] = res.title
            self.summary_dicts[segment_idx]["summary"] = res.summary
            self.summary_dicts[segment_idx]["bullets"] = res.bullets
            self.summary_dicts[segment_idx]["summary_process_text"] = ""


def render_kf_preview_image(idx_kf_pair: list[int, str]) -> rx.Component:
    kf_path = idx_kf_pair[1]
    return rx.image(
        rx.get_upload_url(kf_path),
        width="auto",
        height="100px",
    )


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
                rx.foreach(
                    segment.idx_keyframe_pairs,
                    render_kf_preview_image,
                ),
                gap=10,
                justify="center",
                wrap="wrap",
            ),
            rx.flex(
                status_chip(segment.topic_tags, "info", "blue"),
                justify="center",
                wrap="wrap",
            ),
            rx.button(
                "Summarize",
                align="center",
                on_click=SummaryCardState.generate_summary(segment),
            ),
            rx.cond(
                SummaryCardState.summary_dicts[segment_idx],
                rx.cond(
                    SummaryCardState.summary_dicts[segment_idx].summary_process_text,
                    rx.flex(
                        rx.spinner(size="3"),
                        rx.text(
                            SummaryCardState.summary_dicts[
                                segment_idx
                            ].summary_process_text
                        ),
                        align="center",
                        justify="center",
                        gap=5,
                    ),
                ),
            ),
            rx.cond(
                SummaryCardState.summary_dicts[segment_idx],
                rx.cond(
                    SummaryCardState.summary_dicts[segment_idx].trimmed_video_path,
                    rx.inset(
                        rx.video(
                            url=rx.get_upload_url(
                                SummaryCardState.summary_dicts[
                                    segment_idx
                                ].trimmed_video_path,
                            ),
                            width="640px",
                            height="auto",
                        ),
                    ),
                ),
            ),
            rx.cond(
                SummaryCardState.summary_dicts[segment_idx],
                rx.cond(
                    SummaryCardState.summary_dicts[segment_idx].title,
                    rx.flex(
                        rx.text(
                            SummaryCardState.summary_dicts[segment_idx].title,
                            size="7",
                            align="center",
                        ),
                        rx.flex(
                            rx.foreach(
                                SummaryCardState.summary_dicts[segment_idx].bullets,
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
