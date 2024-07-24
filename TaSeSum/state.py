from TaSeSum.components.upload import UploaderState
import reflex as rx


class Segment(rx.Base):
    text: str
    start: float
    end: float
    topic_id: int
    topic_tags: str
    idx: int
    wordcloud_img_path: str


class CommonState(UploaderState):
    selected_items: list[str]
    segments: list[dict]
    segments_in_view: list[Segment]
    all_items: list[str]
