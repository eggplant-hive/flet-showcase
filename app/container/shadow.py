import flet as ft


def main(page):
  page.add(
    ft.Container(
      content=ft.Text("影付きのコンテナ"),
      width=250,
      height=120,
      bgcolor="white",
      border=ft.border.all(2, "blue"),  # 青いボーダー
      border_radius=20,  # 角を20ピクセル丸める
      shadow=ft.BoxShadow(blur_radius=15, color="gray"),  # グレーの影
      alignment=ft.alignment.center,
    )
  )


ft.app(target=main)
