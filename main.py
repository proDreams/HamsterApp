import flet as ft

from app.main_window import main

if __name__ == "__main__":
    ft.app(
        target=main,
        view=ft.WEB_BROWSER
    )
