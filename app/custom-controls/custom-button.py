import flet as ft


class MyButton(ft.ElevatedButton):
  def __init__(self, text):
    super().__init__()
    self.bgcolor = ft.colors.ORANGE_300  # ボタンの背景色
    self.color = ft.colors.GREEN_800  # ボタンのテキスト色
    self.text = text  # ボタンの表示テキスト


def main(page: ft.Page):
  page.add(MyButton(text="OK"), MyButton(text="Cancel"))


ft.app(main)
