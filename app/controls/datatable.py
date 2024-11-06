import flet as ft


def main(page: ft.Page):
  page.add(
    ft.DataTable(
      width=700,
      bgcolor="yellow",
      border=ft.border.all(2, "red"),
      border_radius=10,
      vertical_lines=ft.BorderSide(3, "blue"),
      horizontal_lines=ft.BorderSide(1, "green"),
      sort_column_index=0,
      sort_ascending=True,
      heading_row_color=ft.colors.BLACK12,
      heading_row_height=100,
      data_row_color={"hovered": "0x30FF0000"},
      show_checkbox_column=True,
      divider_thickness=0,
      column_spacing=200,
      columns=[
        ft.DataColumn(
          ft.Text("アルファベット"),
          on_sort=lambda e: [  # Select the column itself
            e.control.parent.__setattr__("sort_column_index", e.column_index),
            # Toggle the sort (ascending / descending)
            e.control.parent.__setattr__("sort_ascending", False)
            if e.control.parent.sort_ascending
            else e.control.parent.__setattr__("sort_ascending", True),
            # Sort the table rows according above
            e.control.parent.rows.sort(
              key=lambda x: x.cells[e.column_index].content.value,
              reverse=e.control.parent.sort_ascending,
            ),
            # Update table
            e.control.parent.update(),
          ],
        ),
        ft.DataColumn(
          ft.Text("数字"),
          numeric=True,
          on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
        ),
      ],
      rows=[
        ft.DataRow(
          [ft.DataCell(ft.Text("A")), ft.DataCell(ft.Text("1"))],
          selected=True,
          on_select_changed=lambda e: print(f"row select changed: {e.data}"),
        ),
        ft.DataRow([ft.DataCell(ft.Text("B")), ft.DataCell(ft.Text("2"))]),
      ],
    ),
  )


ft.app(target=main)
