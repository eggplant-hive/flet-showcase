import flet as ft


def main(page: ft.Page):
  # ボタンを作成し、on_clickイベントを設定
  button = ft.ElevatedButton(
    text="クリックしてください", on_click=lambda e: button_clicked(e)
  )

  # モーダルダイアログを作成
  dialog = ft.AlertDialog(
    title=ft.Text("通知"),
    content=ft.Text("ボタンがクリックされました！"),
    actions=[ft.TextButton("閉じる", on_click=lambda e: close_dialog())],
  )

  # ダイアログを閉じる関数
  def close_dialog():
    dialog.open = False
    page.update()

  # ボタンがクリックされたときに呼び出される関数
  def button_clicked(e):
    page.dialog = dialog
    dialog.open = True
    page.update()

  # ページにボタンを追加
  page.add(button)


ft.app(target=main)
