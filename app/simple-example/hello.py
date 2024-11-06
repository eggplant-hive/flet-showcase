import flet as ft


def main(page):
  def say_hello(e):
    page.add(ft.Text("こんにちは！"))

  page.add(ft.ElevatedButton("挨拶する", on_click=say_hello))


ft.app(target=main)
