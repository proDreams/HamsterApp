import time
import datetime

from flet import (Page,
                  Text,
                  AppBar,
                  colors,
                  PopupMenuButton,
                  PopupMenuItem,
                  Column,
                  ElevatedButton,
                  CrossAxisAlignment,
                  View,
                  Divider,
                  Container)

from app.timer import Timer
from app.utils import add_to_sheet


def main(page: Page):
    def on_click(e):
        count.value += 2
        last_press.running = False
        last_press.seconds = 0
        last_press.running = True
        content.bgcolor = "red"
        page.update()
        add_to_sheet(count.value)
        time.sleep(15)
        content.bgcolor = "default"
        page.update()

    def clear(e):
        count.value = 0
        page.update()

    app_bar = AppBar(
        title=Text("HamsterApp"),
        center_title=True,
        bgcolor=colors.SURFACE_VARIANT,
        actions=[
            PopupMenuButton(
                items=[
                    PopupMenuItem(
                        text="Сбросить",
                        on_click=clear
                    )
                ]
            )
        ],
    )

    count_btn = ElevatedButton(
        content=Container(
            Text("Добавить 2", size=40)
        ),
        on_click=on_click,
        width=300,
        height=150
    )

    count = Text(
        value=0,
        size=70
    )

    last_press = Timer()

    content = View(
        "/",
        [
            app_bar,
            Column(
                [
                    last_press,
                    Divider(),
                    count_btn,
                    Divider(),
                    count
                ],
                horizontal_alignment=CrossAxisAlignment.CENTER
            )

        ],
        padding=20,
        vertical_alignment="center",
        horizontal_alignment="center"
    )

    page.views.clear()
    page.views.append(
        content
    )

    page.title = 'HamsterApp'
    page.window_width = 375
    page.window_height = 667
    page.update()
