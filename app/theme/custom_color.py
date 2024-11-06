import flet as ft


def main(page: ft.Page):
  # カスタムカラースキームを設定
  custom_color_scheme = ft.ColorScheme(
    primary=ft.colors.GREY,  # プライマリカラー（主要な色）
    secondary=ft.colors.GREEN,  # セカンダリカラー（補助的な色）
    background=ft.colors.LIGHT_BLUE,  # 背景色
    surface=ft.colors.WHITE,  # サーフェスカラー（カードやシートなどの色）
    error=ft.colors.RED,  # エラーカラー（エラーメッセージやエラー状態の色）
    on_primary=ft.colors.WHITE,  # プライマリカラー上のテキストカラー
    on_secondary=ft.colors.BLACK,  # セカンダリカラー上のテキストカラー
    on_background=ft.colors.BLUE_ACCENT,  # 背景色上のテキストカラー
    on_surface=ft.colors.BLACK,  # サーフェスカラー上のテキストカラー
    on_error=ft.colors.WHITE,  # エラーカラー上のテキストカラー
  )

  # Yellow page theme with SYSTEM (default) mode
  page.theme = ft.Theme(
    color_scheme=custom_color_scheme,
  )

  page.add(
    # Page theme
    ft.Container(
      content=ft.ElevatedButton("Page theme button"),
      bgcolor=ft.colors.SURFACE_VARIANT,
      padding=20,
      width=300,
    ),
    # Inherited theme with primary color overridden
    ft.Container(
      theme=ft.Theme(color_scheme=ft.ColorScheme(primary=ft.colors.PINK)),
      content=ft.ElevatedButton("Inherited theme button"),
      bgcolor=ft.colors.SURFACE_VARIANT,
      padding=20,
      width=300,
    ),
    # Unique always DARK theme
    ft.Container(
      theme=ft.Theme(color_scheme_seed=ft.colors.INDIGO),
      theme_mode=ft.ThemeMode.DARK,
      content=ft.ElevatedButton("Unique theme button"),
      bgcolor=ft.colors.SURFACE_VARIANT,
      padding=20,
      width=300,
    ),
  )


ft.app(main)
