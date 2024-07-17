import reflex as rx


class UploaderState(rx.State):
    video_path: str
    progress: int = 0

    def handle_upload_progress(self, progress: dict):
        self.process_text = "Uploading file..."
        self.progress = round(progress["progress"] * 100)

    async def handle_upload(self, files: list[rx.UploadFile]):
        file = files[0]
        upload_data = await file.read()
        self.video_path = rx.get_upload_dir() / file.filename

        with self.video_path.open("wb") as file_object:
            file_object.write(upload_data)


def Uploader() -> rx.Component:
    return rx.container(
        rx.upload(
            rx.flex(
                rx.button(
                    "Select File",
                    color="rgb(107,99,246)",
                    bg="white",
                    border="1px solid rgb(107,99,246)",
                    align="center",
                ),
                rx.text("Choose video file for analysis."),
                width="100%",
                align="center",
                justify="center",
                direction="column",
                gap=10,
            ),
            id="upload",
            border="1px dotted rgb(107,99,246)",
            padding="5em",
            on_drop=UploaderState.handle_upload(
                rx.upload_files(
                    upload_id="upload",
                    on_upload_progress=UploaderState.handle_upload_progress,
                )
            ),
        ),
        rx.cond(
            UploaderState.progress,
            rx.progress(value=UploaderState.progress, max=100),
        ),
        rx.cond(
            UploaderState.video_path,
            rx.text(f"Selected file: {UploaderState.video_path}"),
        ),
        width="100%",
    )
