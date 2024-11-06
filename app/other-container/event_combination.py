import flet as ft


def main(page: ft.Page):
  page.vertical_alignment = ft.MainAxisAlignment.START
  page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

  def on_long_press(e):
    print("on long press")
    page.add(ft.Text("on_long_press triggered", color="red", size=20))

  def on_click(e):
    print("on click")
    page.add(ft.Text("on_click triggered", color="blue", size=40))

  def on_tap_down(e: ft.ContainerTapEvent):
    print("on tap down", e.local_x, e.local_y)
    page.add(
      ft.Text(f"on_tap_down at ({e.local_x}, {e.local_y})", color="green", size=60)
    )

  def on_hover(e):
    page.add(ft.Text("on_hover triggered", color="purple", size=30))

  c = ft.Container(
    bgcolor=ft.colors.RED,
    content=ft.Text("Test Long Press"),
    height=300,
    width=300,
    on_click=on_click,
    on_long_press=on_long_press,
    on_tap_down=on_tap_down,
    on_hover=on_hover,
  )

  page.add(c)


ft.app(main)
