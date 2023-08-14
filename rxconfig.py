import reflex as rx

class DocumentgptConfig(rx.Config):
    pass

config = DocumentgptConfig(
    app_name="documentgpt",
    db_url="sqlite:///reflex.db",
    env=rx.Env.DEV,
    frontend_packages=[
        "react-loading-icons",
    ],
)



