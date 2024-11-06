import asyncio
import random

import flet as ft


class RouletteControl(ft.UserControl):
  def __init__(self, items):
    super().__init__()
    self.items = items  # ルーレットに表示するアイテムのリスト
    self.current_index = 0  # 現在表示されているアイテムのインデックス
    self.is_spinning = True  # ルーレットの回転フラグ

  def build(self):
    # ルーレットの現在の表示を示すラベル
    self.display = ft.Text(
      self.items[self.current_index], size=30, color=ft.colors.BLUE
    )
    return self.display

  async def spin_roulette(self):
    while self.is_spinning:
      # ルーレットを1ステップ進める
      self.current_index = (self.current_index + 1) % len(self.items)
      self.display.value = self.items[self.current_index]
      self.update()  # 画面を更新

      # ルーレット停止の確率チェック
      if random.random() < 0.05:  # 5%の確率で停止
        self.is_spinning = False
        print(f"ルーレットの結果: {self.items[self.current_index]}")
        break

      # 0.05秒ごとに次のアイテムに移動
      await asyncio.sleep(0.05)

  def did_mount(self):
    # ページに追加されたらルーレット開始
    asyncio.create_task(self.spin_roulette())


async def main(page: ft.Page):
  # ルーレットのアイテム
  items = ["🍎", "🍊", "🍌", "🍉", "🍇"]
  page.add(
    ft.Container(
      content=RouletteControl(items),
      width=400,
      padding=ft.padding.all(20),
      alignment=ft.alignment.center,
      bgcolor=ft.colors.GREY_900,
    )
  )


ft.app(target=main)
