from datetime import datetime

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.screen import MDScreen

import work_with_db


class MainScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start = None
        self.stopwatch_time = "00:00:00"
        self.counter = work_with_db.get_or_create_today()

    def on_press(self, e):
        count = int(self.count_lbl.text) + 2
        work_with_db.increase_count(count)
        self.count_lbl.text = str(count)
        self.count()

    def count(self):
        self.start = datetime.now()
        Clock.schedule_interval(self.on_timeout, 1)

    def reset(self):
        work_with_db.reset_today()
        self.count_lbl.text = "0"
        Clock.unschedule(self.on_timeout)
        self.watch_lbl.text = "00:00:00"

    def on_timeout(self, *args):
        d = datetime.now() - self.start
        self.watch_lbl.text = datetime.utcfromtimestamp(d.total_seconds()).strftime("%H:%M:%S")


class SecondScreen(MDScreen):
    pass


class DemoApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_tables = None
        self.title = "HamsterApp"

    def build(self):
        self.theme_cls.theme_style = "Dark"
        return Builder.load_file("main.kv")

    def callback(self, screen):
        self.add_datatable()
        self.root.current = screen

    def add_datatable(self):
        self.data_tables = MDDataTable(
            rows_num=10,
            column_data=[
                ("Дата", dp(35)),
                ("Количество", dp(35)),
            ],
            row_data=work_with_db.get_last()
        )
        self.root.ids.second_scr.ids.data_layout.add_widget(self.data_tables)

    def export(self):
        work_with_db.export_to_google()


if __name__ == "__main__":
    DemoApp().run()
