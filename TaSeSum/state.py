import reflex as rx
from TaSeSum.components.upload import UploaderState


class CommonState(UploaderState):
    selected_items: list[str]
