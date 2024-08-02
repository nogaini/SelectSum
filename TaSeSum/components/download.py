import reflex as rx
from TaSeSum.state import CommonState
from src.downloading import download_video


class DownloaderState(CommonState):
    progress: int = 0
    video_url: str

    @rx.background
    async def handle_download(self, form_data: dict):
        video_url = form_data["url"]
        async with self:
            self.process_button_is_disabled = True
            self.process_text = "Downloading video..."
        video_path = download_video(video_url)
        if not video_path:
            self.process_text = "Download failed. Please refresh and try again."

        if video_path:
            async with self:
                self.video_path = video_path
                self.process_text = ""
                self.process_button_is_disabled = False


def Downloader() -> rx.Component:
    return rx.flex(
        rx.form(
            rx.flex(
                rx.input(placeholder="Try a YouTube URL...", name="url"),
                rx.button(
                    "Fetch video",
                    color="rgb(107,99,246)",
                    bg="white",
                    border="1px solid rgb(107,99,246)",
                    align="center",
                    type="submit",
                ),
                gap=10,
            ),
            width="100%",
            on_submit=DownloaderState.handle_download,
            reset_on_submit=True,
        ),
    )
