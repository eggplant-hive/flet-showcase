import flet as ft


def main(page: ft.Page):
  # AppBarの設定
  page.appbar = ft.AppBar(
    title=ft.Text("Fletアプリケーション"),
    center_title=True,
    bgcolor=ft.colors.BLUE,
    actions=[
      ft.IconButton(
        ft.icons.MENU, on_click=lambda e: print("メニューアイコンがクリックされました")
      )
    ],
  )

  # NavigationRailの設定
  navigation_rail = ft.NavigationRail(
    selected_index=0,
    destinations=[
      ft.NavigationRailDestination(icon=ft.icons.HOME, label="ホーム"),
      ft.NavigationRailDestination(icon=ft.icons.SETTINGS, label="設定"),
      ft.NavigationRailDestination(icon=ft.icons.INFO, label="情報"),
    ],
    on_change=lambda e: print(f"選択されたインデックス: {e.control.selected_index}"),
  )

  # NavigationBarの設定
  navigation_bar = ft.NavigationBar(
    destinations=[
      ft.NavigationDestination(icon=ft.icons.HOME, label="ホーム"),
      ft.NavigationDestination(icon=ft.icons.SEARCH, label="検索"),
      ft.NavigationDestination(icon=ft.icons.ACCOUNT_CIRCLE, label="アカウント"),
    ],
    on_change=lambda e: print(f"選択されたインデックス: {e.control.selected_index}"),
  )

  # ページのレイアウト設定
  page.add(
    ft.Row(
      controls=[
        navigation_rail,
        ft.VerticalDivider(width=1),
        ft.Column(
          controls=[
            ft.Text("メインコンテンツエリア", size=24),
            ft.Container(
              content=ft.Text("ここにコンテンツが表示されます。"),
              alignment=ft.alignment.center,
              bgcolor=ft.colors.LIGHT_BLUE_50,
              padding=20,
              border_radius=10,
              expand=True,
            ),
          ],
          expand=True,
        ),
      ],
      expand=True,
    ),
    navigation_bar,
  )


ft.app(target=main)
