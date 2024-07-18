import reflex as rx
from TaSeSum.components.topic_chips import status_chip


class SummaryCardState(rx.State):
    word_cloud_img_path: str
    tags: str
    video_path: str
    title: str
    bullets: list[str]
    topic_id: int
    in_view: bool = True

    @rx.background
    async def generate_summary(self):
        pass


def render_bullet(bullet: str) -> rx.Component:
    return rx.text(bullet)


def render_summary_card(segment: dict) -> rx.Component:
    return rx.card(
        rx.flex(
            rx.inset(
                rx.image(rx.get_upload_url(segment["wordcloud_img_path"])),
                side="top",
                pb="current",
            ),
            rx.divider(),
            rx.text("Topics"),
            status_chip(segment["topic_tags"], "info", "blue"),
            rx.divider(),
            rx.button("Summarize", on_click=SummaryCardState.generate_summary),
            rx.cond(SummaryCardState.video_path, rx.video(SummaryCardState.video_path)),
            rx.divider(),
            rx.cond(
                SummaryCardState.title,
                rx.flex(
                    rx.text(SummaryCardState.title),
                    rx.foreach(SummaryCardState.bullets, render_bullet),
                    direction="column",
                ),
            ),
            direction="column",
        ),
    )
