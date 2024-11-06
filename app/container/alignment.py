import flet as ft


def main(page):
  page.add(
    ft.Container(
      content=ft.Text("こんにちは、Flet!"),
      width=200,
      height=100,
      bgcolor="lightblue",
      alignment=ft.alignment.center,  # 中央にテキストを配置
    )
  )


ft.app(target=main)
