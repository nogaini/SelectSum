import reflex as rx


class Segment(rx.Base):
    text: str
    start: float
    end: float
    topic_id: int
    topic_tags: str
    idx: int
    wordcloud_img_path: str


class SummaryFields(rx.Base):
    title: str = ""
    summary: str = ""
    bullets: list[str] = []
    trimmed_video_path: str = ""
    summary_process_text: str = ""


class CommonState(rx.State):
    video_path: str
    process_button_is_disabled: bool = True
    process_text: str
    selected_items: list[str]
    segments: list[dict]
    segments_in_view: list[Segment]
    all_items: list[str]
