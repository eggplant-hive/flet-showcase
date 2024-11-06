import flet as ft


def main(page: ft.Page):
  # ボタンのクリックイベント
  def button_clicked(e):
    output_text.value = (
      "ボタンがクリックされました\n"
      f"テキストフィールドの値: {text_field.value}\n"
      f"チェックボックスの状態: {checkbox.value}\n"
      f"選択されたドロップダウンの値: {dropdown.value}\n"
      f"スライダーの値: {slider.value}"
    )
    page.update()

  # TextFieldコントロール
  text_field = ft.TextField(label="テキスト入力欄")

  # Checkboxコントロール
  checkbox = ft.Checkbox(label="チェックボックス")

  # DropDownコントロール
  dropdown = ft.Dropdown(
    label="プルダウンメニュー",
    options=[
      ft.dropdown.Option("オプション1"),
      ft.dropdown.Option("オプション2"),
      ft.dropdown.Option("オプション3"),
    ],
  )

  # Sliderコントロール
  slider = ft.Slider(min=0, max=100, label="スライダー")

  # Buttonコントロール
  button = ft.ElevatedButton(text="送信", on_click=button_clicked)

  # 出力用のTextコントロール
  output_text = ft.Text()

  # ページにコントロールを追加
  page.add(text_field, checkbox, dropdown, slider, button, output_text)


ft.app(target=main)
