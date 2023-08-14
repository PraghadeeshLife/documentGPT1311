"""The main Chat app."""

import reflex as rx
from documentgpt import styles
from documentgpt.components import chat, navbar
from documentgpt.state import State
from .uploadui import uploadui


def index() -> rx.Component:
    return rx.vstack(
        navbar(),
        chat.chat(),
        chat.action_bar(),
        bg=styles.bg_dark_color,
        color=styles.text_light_color,
        min_h="100vh",
        align_items="stretch",
        spacing="0",
    )


# Add state and page to the app.
app = rx.App(state=State, style=styles.base_style)
app.add_page(index)
app.add_page(uploadui)
app.compile()
