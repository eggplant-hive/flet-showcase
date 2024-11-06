import flet as ft


class CRUDRow(ft.UserControl):
  def __init__(self, text, on_update, on_delete):
    super().__init__()
    self.text = text  # 初期のテキスト
    self.on_update = on_update  # 更新コールバック関数
    self.on_delete = on_delete  # 削除コールバック関数

  def build(self):
    # テキストフィールドを作成（初期値として self.text を設定）
    self.text_field = ft.TextField(
      value=self.text,
      expand=True,
      bgcolor=ft.colors.BLACK87,
      color=ft.colors.WHITE,
      border_color=ft.colors.GREY_600,
    )

    # 編集ボタン
    edit_button = ft.IconButton(
      icon=ft.icons.EDIT,
      on_click=self.edit,
      icon_color=ft.colors.AMBER,
    )

    # 更新ボタン
    update_button = ft.IconButton(
      icon=ft.icons.CHECK,
      visible=False,  # 初期状態では非表示
      on_click=self.update,
      icon_color=ft.colors.LIGHT_GREEN,
    )

    # 削除ボタン
    delete_button = ft.IconButton(
      icon=ft.icons.DELETE,
      on_click=self.delete,
      icon_color=ft.colors.RED_ACCENT,
    )

    # ボタンをインスタンス変数として保持
    self.edit_button = edit_button
    self.update_button = update_button

    # 行のレイアウト（テキストフィールドとボタンを横並びに配置）
    return ft.Row(
      controls=[self.text_field, self.edit_button, self.update_button, delete_button]
    )

  def edit(self, e):
    # 編集モードに切り替え
    self.text_field.disabled = False
    self.text_field.focus()
    self.edit_button.visible = False
    self.update_button.visible = True

    # ダイアログの表示 - 編集中の内容を反映
    self.page.dialog = ft.AlertDialog(
      title=ft.Text("編集モードに入りました"),
      content=ft.Text(f"現在のテキスト：{self.text_field.value}"),
      on_dismiss=lambda e: self.page.dialog.close(),
    )
    self.page.dialog.open = True
    self.page.update()

  def update(self, e=None):
    # 更新処理
    if e:  # update ボタンから呼ばれたときのみ実行
      self.text = self.text_field.value
      self.on_update(self)  # 親コンポーネントに通知
    # 編集モード終了
    self.text_field.disabled = True
    self.edit_button.visible = True
    self.update_button.visible = False
    self.page.update()

  def delete(self, e):
    # 削除処理（親コンポーネントに通知）
    self.on_delete(self)


class CRUDApp(ft.UserControl):
  def build(self):
    # 行のリスト
    self.rows = []

    # 行を格納する Column
    self.row_column = ft.Column(
      spacing=5,
    )

    # 新規追加ボタン
    add_button = ft.ElevatedButton(
      text="新しい行を追加",
      on_click=self.add_row,
      bgcolor=ft.colors.BLUE_ACCENT,
      color=ft.colors.WHITE,
    )

    # 全体のレイアウト
    return ft.Column(
      [
        add_button,
        ft.Card(self.row_column, color=ft.colors.BLACK87, margin=ft.margin.all(10)),
      ],
      spacing=5,
    )

  def add_row(self, e):
    # 新しい行を作成し、Column に追加
    new_row = CRUDRow(
      text="新しい項目", on_update=self.update_row, on_delete=self.delete_row
    )
    self.rows.append(new_row)
    self.row_column.controls.append(new_row)
    self.update()  # 画面を更新

  def update_row(self, row):
    # 更新が呼び出された際に通知
    print(f"更新された行のテキスト: {row.text}")

  def delete_row(self, row):
    # 行の削除時に呼ばれる（行をリストと UI から削除）
    self.rows.remove(row)
    self.row_column.controls.remove(row)
    self.update()  # 画面を更新


def main(page: ft.Page):
  # ページのテーマと幅を設定
  page.theme_mode = ft.ThemeMode.DARK
  page.add(
    ft.Container(
      content=CRUDApp(),
      width=600,
      padding=ft.padding.all(5),
      margin=ft.margin.all(10),
      bgcolor=ft.colors.GREY_900,
    )
  )


ft.app(target=main)
