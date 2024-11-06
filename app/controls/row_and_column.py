import flet as ft


def main(page):
  page.add(
    ft.Row(
      controls=[
        ft.Text("左", size=80, color=ft.colors.RED, bgcolor=ft.colors.YELLOW),
        ft.Text("右", size=40, color=ft.colors.WHITE, bgcolor=ft.colors.LIGHT_GREEN),
      ]
    ),
    ft.Column(
      controls=[
        ft.Text("上", size=100, color=ft.colors.WHITE, bgcolor=ft.colors.LIGHT_BLUE),
        ft.Text("下", size=50, color=ft.colors.ORANGE, bgcolor=ft.colors.PINK_100),
      ]
    ),
  )


ft.app(target=main)
