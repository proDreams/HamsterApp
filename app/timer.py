import threading
import time
from flet import (UserControl,
                  Text)


class Timer(UserControl):
    def __init__(self, seconds=0):
        super().__init__()
        self.th = None
        self.running = None
        self.countdown = None
        self.seconds = seconds

    def did_mount(self):
        self.running = True
        self.th = threading.Thread(target=self.update_timer, args=(), daemon=True)
        self.th.start()

    def will_unmount(self):
        self.running = False

    def update_timer(self):
        while self.running:
            mins, secs = divmod(self.seconds, 60)
            self.countdown.value = "{:02d}:{:02d}".format(mins, secs)
            self.update()
            time.sleep(1)
            self.seconds += 1

    def build(self):
        self.countdown = Text(size=70)
        return self.countdown
