import flet as ft


def main(page: ft.Page):
  # テキストフィールドを作成し、on_focusイベントを設定
  focus_field = ft.TextField(
    label="クリックして入力してください", on_focus=lambda e: field_focused(e)
  )

  # フォーカスが当たったときに呼び出される関数
  def field_focused(e):
    page.controls.clear()
    page.add(focus_field)
    page.controls.append(ft.Text("入力欄がフォーカスされました"))
    page.update()

  # ページにテキストフィールドを追加
  page.add(focus_field)


ft.app(target=main)
