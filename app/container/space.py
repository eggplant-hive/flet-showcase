import flet as ft


def main(page):
  page.add(
    ft.Container(
      content=ft.Text("余白とボーダー付きのコンテナ"),
      padding=20,  # 内部に20ピクセルの余白
      margin=10,  # 外部に10ピクセルの余白
      bgcolor="lightgreen",
      border=ft.border.all(3, "green"),  # 緑色の3ピクセルのボーダー
      border_radius=15,  # 角を15ピクセル丸める
      alignment=ft.alignment.center,
    )
  )


ft.app(target=main)
