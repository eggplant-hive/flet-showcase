import random
from math import pi

import flet
from flet import Container, ElevatedButton, Page, Stack, colors


def main(page: Page):
  size = 40
  gap = 6
  duration = 2000  # アニメーションの持続時間

  # カラー定義
  c1 = colors.PINK_500  # "E"の色
  c2 = colors.AMBER_500  # "G"の色
  c3 = colors.LIGHT_GREEN_500  # "G"の色
  c4 = colors.DEEP_PURPLE_500  # "T"の色
  c5 = colors.BLUE_500  # "E"の色
  c6 = colors.ORANGE_500  # "C"と"H"の色

  # 使用する全てのカラー
  all_colors = [
    colors.AMBER_400,
    colors.AMBER_ACCENT_400,
    colors.BLUE_400,
    colors.BROWN_400,
    colors.CYAN_700,
    colors.DEEP_ORANGE_500,
    colors.CYAN_500,
    colors.INDIGO_600,
    colors.ORANGE_ACCENT_100,
    colors.PINK,
    colors.RED_600,
    colors.GREEN_400,
    colors.GREEN_ACCENT_200,
    colors.TEAL_ACCENT_200,
    colors.LIGHT_BLUE_500,
  ]

  # 各文字の構成パーツを定義（(x, y, color)の形式）
  parts = [
    # E
    (0, 0, c1),
    (1, 0, c1),
    (2, 0, c1),
    (0, 1, c1),
    (0, 2, c1),
    (1, 2, c1),
    (2, 2, c1),
    (0, 3, c1),
    (0, 4, c1),
    (1, 4, c1),
    (2, 4, c1),
    # G
    (4, 0, c2),
    (5, 0, c2),
    (6, 0, c2),
    (4, 1, c2),
    (4, 2, c2),
    (6, 2, c2),
    (6, 3, c2),
    (4, 3, c2),
    (5, 3, c2),
    (6, 4, c2),
    (5, 4, c2),
    # G
    (8, 0, c3),
    (9, 0, c3),
    (10, 0, c3),
    (8, 1, c3),
    (8, 2, c3),
    (10, 2, c3),
    (10, 3, c3),
    (8, 3, c3),
    (9, 3, c3),
    (10, 4, c3),
    (9, 4, c3),
    # T
    (12, 0, c4),
    (13, 0, c4),
    (14, 0, c4),
    (13, 1, c4),
    (13, 2, c4),
    (13, 3, c4),
    (13, 4, c4),
    # E
    (16, 0, c5),
    (17, 0, c5),
    (18, 0, c5),
    (16, 1, c5),
    (16, 2, c5),
    (17, 2, c5),
    (18, 2, c5),
    (16, 3, c5),
    (16, 4, c5),
    (17, 4, c5),
    (18, 4, c5),
    # C
    (20, 1, c6),
    (21, 0, c6),
    (22, 0, c6),
    (20, 2, c6),
    (20, 3, c6),
    (21, 4, c6),
    (22, 4, c6),
    # H
    (25, 0, c6),
    (25, 1, c6),
    (25, 2, c6),
    (25, 3, c6),
    (25, 4, c6),
    (26, 2, c6),
    (27, 2, c6),
    (28, 2, c6),
    (27, 0, c6),
    (27, 1, c6),
    (27, 2, c6),
    (27, 3, c6),
    (27, 4, c6),
  ]

  # キャンバスのサイズ
  width = 28 * (size + gap)
  height = 5 * (size + gap)

  # Stackコンテナの作成
  canvas = Stack(
    width=width, height=height, animate_scale=duration, animate_opacity=duration
  )

  # 各パーツをランダムに配置
  for _ in parts:
    canvas.controls.append(
      Container(animate=duration, animate_position=duration, animate_rotation=duration)
    )

  # ランダム配置
  def randomize(e):
    random.seed()
    for i, part in enumerate(parts):
      c = canvas.controls[i]
      part_size = random.randrange(int(size / 2), int(size * 3))
      c.left = random.randrange(0, width)
      c.top = random.randrange(0, height)
      c.bgcolor = all_colors[random.randrange(0, len(all_colors))]
      c.width = part_size
      c.height = part_size
      c.border_radius = random.randrange(0, int(size / 2))
      c.rotate = random.randrange(0, 90) * 2 * pi / 360
    canvas.scale = 5
    canvas.opacity = 0.3
    go_button.visible = True
    again_button.visible = False
    page.update()

  # アニメーションで「EGGTECH」の位置に戻す
  def assemble(e):
    for i, (left, top, bgcolor) in enumerate(parts):
      c = canvas.controls[i]
      c.left = left * (size + gap)
      c.top = top * (size + gap)
      c.bgcolor = bgcolor
      c.width = size
      c.height = size
      c.border_radius = 5
      c.rotate = 0
    canvas.scale = 1
    canvas.opacity = 1
    go_button.visible = False
    again_button.visible = True
    page.update()

  # ボタン作成
  go_button = ElevatedButton("Go!", on_click=assemble)
  again_button = ElevatedButton("Again!", on_click=randomize)

  # 初期状態でランダム配置
  randomize(None)

  # ページの配置設定
  page.horizontal_alignment = "center"
  page.vertical_alignment = "center"
  page.spacing = 30
  page.add(canvas, go_button, again_button)


# アプリ起動
flet.app(main)
