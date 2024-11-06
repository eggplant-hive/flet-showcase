import threading
import time

import flet as ft


class Countdown(ft.Text):
  def __init__(self, seconds):
    super().__init__()
    self.seconds = seconds

  def did_mount(self):
    self.running = True
    self.th = threading.Thread(target=self.update_timer, args=(), daemon=True)
    self.th.start()

  def will_unmount(self):
    self.running = False

  def update_timer(self):
    while self.seconds and self.running:
      mins, secs = divmod(self.seconds, 60)
      self.value = "{:02d}:{:02d}".format(mins, secs)
      self.update()
      time.sleep(1)
      self.seconds -= 1


def main(page: ft.Page):
  page.add(Countdown(120), Countdown(60))


ft.app(target=main)
