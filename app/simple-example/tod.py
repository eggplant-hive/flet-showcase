import flet as ft


# カスタムコントロールの定義
class TaskControl(ft.UserControl):
  def __init__(self, task_text):
    super().__init__()
    self.task_text = task_text

  def build(self):
    return ft.Row([ft.Checkbox(), ft.Text(value=self.task_text)])


def main(page):
  tasks = []

  def add_task(e):
    task_control = TaskControl(new_task.value)
    tasks.append(task_control)
    task_list.controls.append(task_control)
    new_task.value = ""
    page.update()

  new_task = ft.TextField(label="新しいタスクを追加", width=600)
  task_list = ft.Column()

  page.add(new_task, ft.ElevatedButton("追加", on_click=add_task), task_list)


ft.app(target=main)
