import reflex as rx
from reflex.components.radix.themes.base import (
    LiteralAccentColor,
)
from TaSeSum.state import CommonState

chip_props = {
    "radius": "full",
    "variant": "surface",
    "size": "3",
    "cursor": "pointer",
    "style": {"_hover": {"opacity": 0.75}},
}

status_chip_props = {
    "radius": "full",
    "variant": "outline",
    "size": "3",
}


class TopicChipsState(CommonState):
    def update_segments_in_view(self):
        self.segments_in_view = [
            segment
            for segment in self.segments
            if segment["topic_tags"] in self.selected_items
        ]

    def add_selected(self, item: str):
        self.selected_items.append(item)
        self.update_segments_in_view()

    def remove_selected(self, item: str):
        self.selected_items.remove(item)
        self.update_segments_in_view()

    def add_all_selected(self):
        self.selected_items = [segment["topic_tags"] for segment in self.segments]
        self.update_segments_in_view()

    def clear_selected(self):
        self.selected_items.clear()
        self.update_segments_in_view()


def action_button(
    icon: str,
    label: str,
    on_click: callable,
    color_scheme: LiteralAccentColor,
) -> rx.Component:
    return rx.button(
        rx.icon(icon, size=16),
        label,
        variant="soft",
        size="2",
        on_click=on_click,
        color_scheme=color_scheme,
        cursor="pointer",
    )


def status_chip(status: str, icon: str, color: LiteralAccentColor) -> rx.Component:
    return rx.badge(
        rx.icon(icon, size=18),
        status,
        color_scheme=color,
        **status_chip_props,
    )


def selected_item_chip(item: str) -> rx.Component:
    return rx.badge(
        item,
        rx.icon("circle-x", size=18),
        color_scheme="green",
        **chip_props,
        on_click=TopicChipsState.remove_selected(item),
    )


def unselected_item_chip(item: str) -> rx.Component:
    return rx.cond(
        TopicChipsState.selected_items.contains(item),
        rx.fragment(),
        rx.badge(
            item,
            rx.icon("circle-plus", size=18),
            color_scheme="gray",
            **chip_props,
            on_click=TopicChipsState.add_selected(item),
        ),
    )


def TopicChipsSelector() -> rx.Component:
    return rx.vstack(
        rx.flex(
            rx.hstack(
                rx.heading(
                    "Selected Topics" + f" ({TopicChipsState.selected_items.length()})",
                    size="4",
                ),
                spacing="1",
                align="center",
                width="100%",
                justify_content=["end", "start"],
            ),
            rx.hstack(
                action_button(
                    "plus",
                    "Add All",
                    TopicChipsState.add_all_selected,
                    "green",
                ),
                action_button(
                    "trash",
                    "Clear All",
                    TopicChipsState.clear_selected,
                    "tomato",
                ),
                spacing="2",
                justify="end",
                width="100%",
            ),
            justify="between",
            flex_direction=["column", "row"],
            align="center",
            spacing="2",
            margin_bottom="10px",
            width="100%",
        ),
        # Selected Items
        rx.flex(
            rx.foreach(
                TopicChipsState.selected_items,
                selected_item_chip,
            ),
            wrap="wrap",
            spacing="2",
            justify_content="start",
        ),
        rx.divider(),
        # Unselected Items
        rx.flex(
            rx.foreach(TopicChipsState.all_items, unselected_item_chip),
            wrap="wrap",
            spacing="2",
            justify_content="start",
        ),
        justify_content="start",
        align_items="start",
        width="100%",
    )
