import flet as ft


def main(page):
  # ListViewを作成し、複数のテキスト要素を追加
  list_view = ft.ListView(
    controls=[ft.Text(f"アイテム {i}") for i in range(1, 21)],
    height=300,  # スクロール可能な高さを設定
  )

  page.add(list_view)


ft.app(target=main)
