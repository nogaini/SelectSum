import reflex as rx


class SummaryCardState(rx.State):
    word_cloud_img_path: str
    tags: list[str]
    video_path: str
    title: str
    bullets: list[str]
    topic_id: int
    in_view: bool = True


def render_summary_card(segment: list[dict]) -> rx.Component:
    pass


def SummaryCard() -> rx.Component:
    pass
