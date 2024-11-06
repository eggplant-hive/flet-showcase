import flet as ft


def main(page: ft.Page):
  # テキストフィールドを作成し、on_submitイベントを設定
  name_field = ft.TextField(
    label="お名前を入力してください", on_submit=lambda e: name_submitted(e)
  )

  # テキストフィールドが送信されたときに呼び出される関数
  def name_submitted(e):
    entered_name = e.control.value
    page.controls.clear()
    name_field.value = ""
    page.add(name_field)
    page.controls.append(ft.Text(f"入力された名前: {entered_name}"))
    page.update()

  # ページにテキストフィールドを追加
  page.add(name_field)


ft.app(target=main)
