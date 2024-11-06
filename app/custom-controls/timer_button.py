import threading
import time

import flet as ft


class Countdown(ft.Text):
  def __init__(self, seconds):
    super().__init__(value=self.format_time(seconds), size=40)
    self.initial_seconds = seconds
    self.seconds = seconds
    self.running = False
    self.thread = None

  def format_time(self, seconds):
    mins, secs = divmod(seconds, 60)
    return f"{mins:02d}:{secs:02d}"

  def start(self):
    if not self.running and self.seconds > 0:
      self.running = True
      self.thread = threading.Thread(target=self.update_timer, daemon=True)
      self.thread.start()

  def pause(self):
    self.running = False

  def reset(self):
    self.pause()
    self.seconds = self.initial_seconds
    self.value = self.format_time(self.seconds)
    self.update()

  def update_timer(self):
    while self.seconds > 0 and self.running:
      self.value = self.format_time(self.seconds)
      self.update()
      time.sleep(1)
      self.seconds -= 1
    if self.seconds == 0:
      self.value = "00:00"
      self.update()
    self.running = False


def main(page: ft.Page):
  page.title = "カウントダウンタイマー"

  # カウントダウンタイマー1（120秒）
  countdown1 = Countdown(120)
  btn_start1 = ft.ElevatedButton("スタート", on_click=lambda e: countdown1.start())
  btn_pause1 = ft.ElevatedButton("停止", on_click=lambda e: countdown1.pause())
  btn_reset1 = ft.ElevatedButton("リセット", on_click=lambda e: countdown1.reset())

  layout1 = ft.Column(
    [
      countdown1,
      ft.Row(
        [btn_start1, btn_pause1, btn_reset1],
        spacing=10,
        alignment=ft.MainAxisAlignment.CENTER,
      ),
    ],
    alignment=ft.MainAxisAlignment.START,
    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    spacing=20,
  )

  # カウントダウンタイマー2（60秒）
  countdown2 = Countdown(60)
  btn_start2 = ft.ElevatedButton("スタート", on_click=lambda e: countdown2.start())
  btn_pause2 = ft.ElevatedButton("停止", on_click=lambda e: countdown2.pause())
  btn_reset2 = ft.ElevatedButton("リセット", on_click=lambda e: countdown2.reset())

  layout2 = ft.Column(
    [
      countdown2,
      ft.Row(
        [btn_start2, btn_pause2, btn_reset2],
        spacing=10,
        alignment=ft.MainAxisAlignment.CENTER,
      ),
    ],
    alignment=ft.MainAxisAlignment.START,
    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    spacing=20,
  )

  # ページにレイアウトを追加
  page.add(
    ft.Column(
      [layout1, layout2],
      alignment=ft.MainAxisAlignment.CENTER,
      horizontal_alignment=ft.CrossAxisAlignment.CENTER,
      spacing=40,
    )
  )


ft.app(target=main)
