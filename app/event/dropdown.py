import flet as ft


def main(page: ft.Page):
  # ドロップダウンメニューの作成
  dropdown = ft.Dropdown(
    options=[
      ft.dropdown.Option("apple", "りんご"),
      ft.dropdown.Option("banana", "バナナ"),
      ft.dropdown.Option("orange", "オレンジ"),
    ],
    label="好きな果物を選んでください",
    on_change=lambda e: dropdown_changed(e),
  )

  # イベントが発生したときに呼び出される関数
  def dropdown_changed(e):
    selected_fruit = e.control.value
    page.controls.clear()
    page.add(dropdown)  # ドロップダウンメニューを再追加
    page.controls.append(ft.Text(f"選択した果物: {selected_fruit}"))
    page.update()  # ページを更新して表示を反映

  # ページにドロップダウンを追加
  page.add(dropdown)


ft.app(target=main)
