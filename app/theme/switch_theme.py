import flet as ft


def main(page: ft.Page):
  # テーマ切り替え関数
  def toggle_theme(e):
    if page.theme_mode == ft.ThemeMode.LIGHT:
      page.theme_mode = ft.ThemeMode.DARK
    else:
      page.theme_mode = ft.ThemeMode.LIGHT
    page.update()  # 変更を反映

  # ボタンをクリックでテーマを切り替え
  toggle_button = ft.ElevatedButton("テーマを切り替える", on_click=toggle_theme)
  page.add(toggle_button)

  # 初期テーマとしてライトテーマを設定
  page.theme_mode = ft.ThemeMode.LIGHT


ft.app(target=main)
