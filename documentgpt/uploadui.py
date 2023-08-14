import reflex as rx
from documentgpt import styles
from documentgpt.components import navbar
from documentgpt.state import State


def uploadui() -> rx.Component:
    return rx.vstack(
        navbar(),
        rx.spacer(),
        rx.center(
            rx.container(
                rx.upload(
                        rx.vstack(
                            rx.button(
                                "Select File",
                                bg=styles.accent_color,
                                px="4",
                                py="2",
                                h="auto",
                            ),
                            rx.text(
                                "Drag and drop files here or click to select files"
                            ),
                        ),
                        accept={
                            "text/plain": [".txt"],
                            "application/pdf": [".pdf"]
                        },
                        border=f"1px dotted white",
                        padding="5em",
                    ),
                    rx.box(
                        padding=5,
                    ),
                    rx.cond(
                    State.upload_processing,
                    rx.circular_progress(is_indeterminate=True),
                    rx.button(
                        "Upload",
                        bg=styles.accent_color,
                        px="4",
                        py="2",
                        h="auto",
                        on_click=lambda: State.handle_upload(
                            rx.upload_files()
                        ),
                    ),),
                center_content = True,
            ),
        ),
        rx.spacer(),
        bg=styles.bg_dark_color,
        color=styles.text_light_color,
        min_h="100vh",
        align_items="stretch",
        spacing="0"
    )



