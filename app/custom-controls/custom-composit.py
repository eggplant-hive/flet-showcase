import flet as ft


class MyButton(ft.ElevatedButton):
  def __init__(self, text, on_click):
    super().__init__()
    self.bgcolor = ft.colors.ORANGE_300
    self.color = ft.colors.GREEN_800
    self.text = text
    self.on_click = on_click


# カスタムコントロール MyButtonRow を定義
class MyButtonRow(ft.Column):
  def __init__(self):
    super().__init__()

    # テキストを表示するコンテナをカスタムコントロール内に作成
    self.text_container = ft.Column()

    # イベントハンドラの定義
    def ok_clicked(e):
      self.text_container.controls.clear()
      self.text_container.controls.append(ft.Text("OK clicked"))
      self.update()

    def cancel_clicked(e):
      self.text_container.controls.clear()
      self.text_container.controls.append(ft.Text("Cancel clicked"))
      self.update()

    # Row内にOKボタンとCancelボタンを追加
    self.controls.append(
      ft.Row(
        [
          MyButton(text="OK", on_click=ok_clicked),
          MyButton(text="Cancel", on_click=cancel_clicked),
        ]
      )
    )

    # テキストコンテナをカスタムコントロールに追加
    self.controls.append(self.text_container)


# メイン関数でカスタムコントロールを利用
def main(page: ft.Page):
  page.add(MyButtonRow())


ft.app(main)
