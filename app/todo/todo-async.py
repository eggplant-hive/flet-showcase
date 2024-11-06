import flet as ft


class Task(ft.Column):
  def __init__(self, task_name, task_status_change, task_delete):
    super().__init__()
    self.completed = False
    self.task_name = task_name
    self.task_status_change = task_status_change
    self.task_delete = task_delete
    self.display_task = ft.Checkbox(
      value=False, label=self.task_name, on_change=self.status_changed
    )
    self.edit_name = ft.TextField(expand=1)

    self.display_view = ft.Row(
      alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
      vertical_alignment=ft.CrossAxisAlignment.CENTER,
      controls=[
        self.display_task,
        ft.Row(
          spacing=0,
          controls=[
            ft.IconButton(
              icon=ft.icons.CREATE_OUTLINED,
              tooltip="Edit To-Do",
              on_click=self.edit_clicked,
            ),
            ft.IconButton(
              ft.icons.DELETE_OUTLINE,
              tooltip="Delete To-Do",
              on_click=self.delete_clicked,
            ),
          ],
        ),
      ],
    )

    self.edit_view = ft.Row(
      visible=False,
      alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
      vertical_alignment=ft.CrossAxisAlignment.CENTER,
      controls=[
        self.edit_name,
        ft.IconButton(
          icon=ft.icons.DONE_OUTLINE_OUTLINED,
          icon_color=ft.colors.GREEN,
          tooltip="Update To-Do",
          on_click=self.save_clicked,
        ),
      ],
    )
    self.controls = [self.display_view, self.edit_view]

  async def edit_clicked(self, e):
    self.edit_name.value = self.display_task.label
    self.display_view.visible = False
    self.edit_view.visible = True
    await self.update_async()

  async def save_clicked(self, e):
    self.display_task.label = self.edit_name.value
    self.display_view.visible = True
    self.edit_view.visible = False
    await self.update_async()

  async def status_changed(self, e):
    self.completed = self.display_task.value
    await self.task_status_change(self)

  async def delete_clicked(self, e):
    await self.task_delete(self)


class TodoApp(ft.Column):
  def __init__(self):
    super().__init__()
    self.new_task = ft.TextField(
      hint_text="何をする必要がありますか？", on_submit=self.add_clicked, expand=True
    )
    self.tasks = ft.Column()

    self.filter = ft.Tabs(
      scrollable=False,
      selected_index=0,
      on_change=self.tabs_changed,
      tabs=[ft.Tab(text="すべて"), ft.Tab(text="アクティブ"), ft.Tab(text="完了済み")],
    )

    self.items_left = ft.Text("0 件のタスクが残っています")

    self.width = 600
    self.controls = [
      ft.Row(
        [ft.Text(value="ToDoアプリ", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM)],
        alignment=ft.MainAxisAlignment.CENTER,
      ),
      ft.Row(
        controls=[
          self.new_task,
          ft.FloatingActionButton(icon=ft.icons.ADD, on_click=self.add_clicked),
        ],
      ),
      ft.Column(
        spacing=25,
        controls=[
          self.filter,
          self.tasks,
          ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
              self.items_left,
              ft.OutlinedButton(
                text="完了したタスクを削除", on_click=self.clear_clicked
              ),
            ],
          ),
        ],
      ),
    ]

  async def add_clicked(self, e):
    if self.new_task.value:
      task = Task(self.new_task.value, self.task_status_change, self.task_delete)
      self.tasks.controls.append(task)
      self.new_task.value = ""
      await self.new_task.focus_async()
      await self.update_async()

  async def task_status_change(self, task):
    await self.before_update()
    await self.update_async()

  async def task_delete(self, task):
    self.tasks.controls.remove(task)
    await self.before_update()
    await self.update_async()

  async def tabs_changed(self, e):
    await self.before_update()  # タブ変更時にタスクの表示を更新
    await self.update_async()

  async def clear_clicked(self, e):
    for task in self.tasks.controls[:]:
      if task.completed:
        await self.task_delete(task)

  async def before_update(self):
    status = self.filter.tabs[self.filter.selected_index].text
    count = 0
    for task in self.tasks.controls:
      task.visible = (
        status == "すべて"
        or (status == "アクティブ" and not task.completed)
        or (status == "完了済み" and task.completed)
      )
      if not task.completed:
        count += 1
    self.items_left.value = f"{count} 件のタスクが残っています"


async def main(page: ft.Page):
  page.title = "ToDoアプリ"
  page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
  page.scroll = ft.ScrollMode.ADAPTIVE

  # アプリのコントロールを作成しページに追加
  await page.add_async(TodoApp())


ft.app(main)
