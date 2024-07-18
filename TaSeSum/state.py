from TaSeSum.components.upload import UploaderState


class CommonState(UploaderState):
    selected_items: list[str]
    segments: list[dict]
    segments_in_view: list[dict]
