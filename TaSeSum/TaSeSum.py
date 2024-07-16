import reflex as rx
from TaSeSum.components.upload import UploadComponent, UploadState


class State(UploadState):
    @rx.background
    async def process_video(self):
        async with self:
            print(self.video_path)


def index() -> rx.Component:
    return rx.flex(
        UploadComponent(),
        rx.cond(
            State.video_path,
            rx.button("Process", type="submit", on_click=State.process_video),
        ),
        align="center",
        justify="center",
        direction="column",
        margin=20,
        gap=20,
    )


app = rx.App()
app.add_page(index)
