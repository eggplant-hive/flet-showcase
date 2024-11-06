import flet as ft


class MyButton(ft.ElevatedButton):
  def __init__(self, text, on_click):
    super().__init__()
    self.bgcolor = ft.colors.ORANGE_300
    self.color = ft.colors.GREEN_800
    self.text = text
    self.on_click = on_click


def main(page: ft.Page):
  # テキストを表示するためのコンテナ
  text_container = ft.Column()

  def ok_clicked(e):
    text_container.controls.clear()
    text_container.controls.append(ft.Text("OK clicked"))
    page.update()

  def cancel_clicked(e):
    text_container.controls.clear()
    text_container.controls.append(ft.Text("Cancel clicked"))
    page.update()

  page.add(
    ft.Row(
      [
        MyButton(text="OK", on_click=ok_clicked),
        MyButton(text="Cancel", on_click=cancel_clicked),
      ]
    ),
    text_container,
  )


ft.app(main)
