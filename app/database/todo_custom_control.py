from typing import List, Optional

import flet as ft
from sqlmodel import Field, Session, SQLModel, create_engine, select

DB_PATH = "sqlite:///todo.db"


class Todo(SQLModel, table=True):
  __tablename__ = "todos"
  id: Optional[int] = Field(default=None, primary_key=True)
  task: str
  completed: bool = False


class TodoManager:
  def __init__(self, db_path: str = DB_PATH):
    self.engine = create_engine(db_path)

  def init_db(self):
    SQLModel.metadata.create_all(self.engine, checkfirst=True)

  def fetch_data(self, completed: Optional[bool] = None) -> List[Todo]:
    with Session(self.engine) as session:
      statement = select(Todo)
      if completed is not None:
        statement = statement.where(Todo.completed == completed)
      results = session.exec(statement)
      return results.all()

  def insert_data(self, task: str):
    todo = Todo(task=task)
    with Session(self.engine) as session:
      session.add(todo)
      session.commit()

  def update_data(self, task_id: int, updates: dict):
    if not updates:
      raise ValueError("更新するカラムが指定されていません。")

    allowed_columns = {"task", "completed"}
    invalid_columns = set(updates.keys()) - allowed_columns
    if invalid_columns:
      raise ValueError(f"無効なカラム名です: {', '.join(invalid_columns)}")

    with Session(self.engine) as session:
      todo = session.get(Todo, task_id)
      if not todo:
        raise ValueError("タスクが見つかりません。")
      for key, value in updates.items():
        setattr(todo, key, value)
      session.commit()

  def delete_data(self, task_id: int):
    with Session(self.engine) as session:
      todo = session.get(Todo, task_id)
      if todo:
        session.delete(todo)
        session.commit()


todo_manager = TodoManager()


class TaskRow(ft.DataRow):
  def __init__(
    self,
    task_id,
    task_name,
    completed,
    is_editing,
    enter_edit_mode,
    save_edited_task,
    delete_task,
    toggle_task_status,
  ):
    self.task_id = task_id
    self.delete_task = delete_task
    self.save_edited_task = save_edited_task
    self.toggle_task_status = toggle_task_status

    task_completed_checkbox = ft.Checkbox(
      value=(completed == 1),  # データベースから取得した値を反映
      on_change=lambda e, task_id=task_id: self.on_toggle_task_status(e, task_id),
    )

    cells = [
      ft.DataCell(task_completed_checkbox),
      ft.DataCell(ft.Text(str(task_id))),  # ID
    ]

    if is_editing:
      # 編集モードのUI
      task_field = ft.TextField(value=task_name, expand=True)
      save_button = ft.IconButton(
        icon=ft.icons.SAVE,  # 保存アイコンを設定
        on_click=lambda e,
        task_id=task_id,
        new_task_name=task_field.value: self.on_save_edited_task(
          e, task_id, task_field.value
        ),
      )
      cells.extend([ft.DataCell(task_field), ft.DataCell(ft.Row([save_button]))])
    else:
      # 通常モードのUI
      cells.extend(
        [
          ft.DataCell(
            ft.Text(task_name),
            on_tap=lambda e: enter_edit_mode(task_id),
          ),  # 編集可能なタスク名
          ft.DataCell(
            ft.Row(
              [
                ft.IconButton(
                  ft.icons.EDIT,
                  on_click=lambda e: enter_edit_mode(task_id),
                ),  # 編集ボタン
                ft.IconButton(
                  ft.icons.DELETE,
                  on_click=lambda e, task_id=task_id: self.on_delete_task(e, task_id),
                ),  # 削除ボタン
              ]
            )
          ),
        ]
      )

    super().__init__(cells=cells)

  def on_delete_task(self, e, task_id):
    todo_manager.delete_data(task_id)
    self.delete_task(task_id)

  def on_save_edited_task(self, e, task_id, new_task_name):
    if new_task_name:
      todo_manager.update_data(task_id, {"task": new_task_name})
    self.save_edited_task(task_id, new_task_name)

  def on_toggle_task_status(self, e, task_id):
    completed = e.control.value
    todo_manager.update_data(task_id, {"completed": completed})
    self.toggle_task_status(task_id, completed)


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
    completed = self.current_tab == "DONE"

    data = todo_manager.fetch_data(completed=completed)
    self.data_table.rows.clear()

    for todo in data:
      task_id = todo.id
      task_name = todo.task
      completed = todo.completed

      is_editing = task_id == self.editing_row_id  # タスクが編集モードかどうかを判断

      # タブに基づいて表示するデータをフィルタリング
      self.data_table.rows.append(
        TaskRow(
          task_id=task_id,
          task_name=task_name,
          completed=completed,
          is_editing=is_editing,
          enter_edit_mode=self.enter_edit_mode,
          save_edited_task=self.save_edited_task,
          delete_task=self.delete_task,
          toggle_task_status=self.toggle_task_status,
        )
      )

    self.page.update()

  def toggle_task_status(self, task_id, completed):
    self.load_data()  # チェックボックスの状態変更後にデータを再読み込み

  def enter_edit_mode(self, task_id):
    self.editing_row_id = task_id
    self.load_data()

  def save_edited_task(self, task_id, new_task_name):
    self.editing_row_id = None  # 編集モードを解除
    self.load_data()

  def add_task(self, e):
    task_name = self.task_field.value
    if task_name:
      self.task_field.value = ""
      # 保存したら タブを "TODO" に変更
      self.current_tab = "TODO"
      self.tabs.selected_index = 0

      todo_manager.insert_data(task_name)
      self.load_data()

  def delete_task(self, task_id):
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
todo_manager.init_db()

# Fletアプリの起動
ft.app(target=main)
