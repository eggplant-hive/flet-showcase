import flet as ft


def main(page: ft.Page):
  stack_control = ft.Stack(
    width=500,
    height=500,
    controls=[
      ft.Container(width=300, height=300, bgcolor=ft.colors.RED),
      ft.Container(width=50, height=50, bgcolor=ft.colors.BLUE, left=25, top=25),
    ],
  )
  page.add(stack_control)


ft.app(target=main)
