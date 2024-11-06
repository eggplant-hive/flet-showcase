import flet as ft
import flet.canvas as cv


def main(page: ft.Page):
  # Textコントロール
  text_control = ft.Text("こんにちは、Flet!")

  # Imageコントロール
  image_control = ft.Image(src="https://picsum.photos/200/200", width=200, height=200)

  canvas_control = cv.Canvas(
    width=200,
    height=200,
    shapes=[
      cv.Rect(
        50, 50, 100, 100, paint=ft.Paint(color=ft.colors.RED)
      ),  # 塗りつぶしの色指定
      cv.Circle(
        100, 100, 50, paint=ft.Paint(color=ft.colors.BLUE)
      ),  # 塗りつぶしの色指定
    ],
  )

  # Markdownコントロール
  markdown_control = ft.Markdown(
    """
# Markdownの例
これは**Markdown**形式のテキストです。
- リストアイテム1
- リストアイテム2
    """
  )

  # ページにコントロールを追加
  page.add(text_control, image_control, canvas_control, markdown_control)


ft.app(target=main)
