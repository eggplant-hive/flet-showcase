import sqlite3

import flet as ft

DB_PATH = "todo.db"
TODOS_TABLE = "todos"


# SQLiteデータベースのセットアップ
def init_db():
  conn = sqlite3.connect(DB_PATH)
  cursor = conn.cursor()
  cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {TODOS_TABLE} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            completed BOOLEAN NOT NULL DEFAULT 0
        )
    """)
  conn.commit()
  conn.close()


# SQLiteからデータを取得
def fetch_data():
  conn = sqlite3.connect(DB_PATH)
  cursor = conn.cursor()
  cursor.execute(f"SELECT * FROM {TODOS_TABLE}")
  data = cursor.fetchall()
  conn.close()
  return data


# SQLiteに新しいレコードを挿入
def insert_data(task):
  conn = sqlite3.connect(DB_PATH)
  cursor = conn.cursor()
  cursor.execute(
    f"INSERT INTO {TODOS_TABLE} (task, completed) VALUES (?, ?)", (task, False)
  )
  conn.commit()
  conn.close()


def update_data(task_id, updates):
  """
  タスクを更新。

  Parameters:
      task_id (int): 更新対象のタスクID。
      updates (dict): 更新するカラム名と新しい値の辞書。
      例: {'task': '新しいタスク名', 'completed': True}
  """
  if not updates:
    raise ValueError("更新するカラムが指定されていません。")

  allowed_columns = {"task", "completed"}  # 更新を許可するカラムを定義

  # 更新要求に含まれるカラム名が許可されたものか確認
  invalid_columns = set(updates.keys()) - allowed_columns
  if invalid_columns:
    raise ValueError(f"無効なカラム名です: {', '.join(invalid_columns)}")

  # SET句の動的生成
  set_clause = ", ".join([f"{column} = ?" for column in updates.keys()])
  values = list(updates.values())
  values.append(task_id)  # WHERE句のidに対応する値を追加

  query = f"UPDATE {TODOS_TABLE} SET {set_clause} WHERE id = ?"

  # データベース接続とクエリの実行
  conn = sqlite3.connect(DB_PATH)
  cursor = conn.cursor()
  cursor.execute(query, values)
  conn.commit()
  conn.close()


# SQLiteのデータを削除
def delete_data(task_id):
  conn = sqlite3.connect(DB_PATH)
  cursor = conn.cursor()
  cursor.execute(f"DELETE FROM {TODOS_TABLE} WHERE id = ?", (task_id,))
  conn.commit()
  conn.close()


class TodoApp:
  def __init__(self, page):
    self.page = page
    self.page.title = "TODO App with SQLite and Flet"
    self.editing_row_id = None
    self.current_tab = "TODO"
    self.tabs = None

    # DataTableの定義
    self.data_table = ft.DataTable(
      columns=[
        ft.DataColumn(ft.Text("完了？")),
        ft.DataColumn(ft.Text("ID")),
        ft.DataColumn(ft.Text("タスク名")),
        ft.DataColumn(ft.Text("Actions")),  # アクション用の列
      ],
      rows=[],
    )

    # タスク追加用のテキストフィールド
    self.task_field = ft.TextField(label="新しいタスク", width=600)

    # ボタン定義
    self.add_button = ft.FloatingActionButton(icon=ft.icons.ADD, on_click=self.add_task)

    # Rowコンポーネントを使用して横に並べる
    self.task_row = ft.Row(
      controls=[self.task_field, self.add_button],
      spacing=10,  # 要素間のスペースを設定
    )

    # TODO/DONEのタブを追加
    self.tabs = ft.Tabs(
      selected_index=0,  # 初期選択はTODOタブ
      tabs=[
        ft.Tab(text="TODO"),
        ft.Tab(text="DONE"),
      ],
      width=700,
      on_change=self.switch_tab,  # タブ切り替えイベント
    )

    # ページにコンポーネントを追加
    self.page.add(self.task_row, self.tabs, self.data_table)

    # 初期データの読み込み
    self.load_data()

  def load_data(self):
    data = fetch_data()
    self.data_table.rows.clear()

    for row in data:
      task_id = row[0]
      task_name = row[1]
      completed = row[2]  # データベースから取得したcompleted値

      task_completed_checkbox = ft.Checkbox(
        value=(completed == 1),  # データベースから取得した値を反映
        on_change=lambda e, task_id=task_id: self.toggle_task_status(
          task_id, e.control.value
        ),
      )

      cells = [
        ft.DataCell(task_completed_checkbox),
        ft.DataCell(ft.Text(str(task_id))),  # ID
      ]

      # タブに基づいて表示するデータをフィルタリング
      if (self.current_tab == "TODO" and not completed) or (
        self.current_tab == "DONE" and completed
      ):
        # 編集モードかどうかを判断
        if task_id == self.editing_row_id:
          # 編集モードのUI
          task_field = ft.TextField(value=task_name, expand=True)
          save_button = ft.IconButton(
            icon=ft.icons.SAVE,  # 保存アイコンを設定
            on_click=lambda e,
            task_id=task_id,
            task_field=task_field: self.save_edited_task(task_id, task_field.value),
          )

          # 編集用のテキストフィールド + 保存ボタン
          cells.extend([ft.DataCell(task_field), ft.DataCell(ft.Row([save_button]))])

        else:
          # 通常モードのUI
          cells.extend(
            [
              ft.DataCell(
                ft.Text(task_name),
                on_tap=lambda e, task_id=task_id: self.enter_edit_mode(task_id),
              ),  # 編集可能なタスク名
              ft.DataCell(
                ft.Row(
                  [
                    ft.IconButton(
                      ft.icons.EDIT,
                      on_click=lambda e, task_id=task_id: self.enter_edit_mode(task_id),
                    ),  # 編集ボタン
                    ft.IconButton(
                      ft.icons.DELETE,
                      on_click=lambda e, task_id=task_id: self.delete_task(task_id),
                    ),  # 削除ボタン
                  ]
                )
              ),
            ]
          )
        self.data_table.rows.append(ft.DataRow(cells=cells))

    self.page.update()

  def toggle_task_status(self, task_id, completed):
    update_data(task_id, {"completed": completed})
    self.load_data()  # チェックボックスの状態変更後にデータを再読み込み

  def enter_edit_mode(self, task_id):
    self.editing_row_id = task_id
    self.load_data()

  def save_edited_task(self, task_id, new_task_name):
    if new_task_name:
      update_data(task_id, {"task": new_task_name})
    self.editing_row_id = None  # 編集モードを解除
    self.load_data()

  def add_task(self, e):
    task_name = self.task_field.value
    if task_name:
      insert_data(task_name)
      self.task_field.value = ""
      # 保存したら タブを "TODO" に変更
      self.current_tab = "TODO"
      self.tabs.selected_index = 0
      self.load_data()

  def delete_task(self, task_id):
    delete_data(task_id)
    self.load_data()

  def switch_tab(self, e):
    selected_index = e.control.selected_index
    self.current_tab = e.control.tabs[
      selected_index
    ].text  # 選択されたタブのテキストを取得して切り替え
    self.load_data()


# Fletのメインアプリ
def main(page: ft.Page):
  TodoApp(page)


# SQLiteの初期化
init_db()

# Fletアプリの起動
ft.app(target=main)
