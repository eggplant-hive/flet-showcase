import flet as ft
import requests

# ショップの種類と日本語の対応表
shop_types = {
  "supermarket": "スーパーマーケット",
  "bakery": "ベーカリー",
  "butcher": "精肉店",
  "clothes": "衣料品店",
  "electronics": "電子機器店",
  "furniture": "家具店",
  "hairdresser": "美容院",
  "chemist": "薬局",
  "convenience": "コンビニエンスストア",
  "florist": "花屋",
  "greengrocer": "八百屋",
  "jewelry": "宝石店",
  "optician": "眼鏡店",
  "shoes": "靴屋",
  "sports": "スポーツ用品店",
  "stationery": "文房具店",
  "toys": "おもちゃ屋",
}


def main(page: ft.Page):
  page.title = "ショップ表示アプリ (OpenStreetMap)"

  # Overpass APIからデータを取得する関数（緯度・経度を基にショップ検索）
  def fetch_shops(shop_type, lat, lon):
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = f"""
        [out:json];
        node
          ["shop"="{shop_type}"]
          (around:500,{lat},{lon});
        out body;
        """
    response = requests.get(overpass_url, params={"data": overpass_query})
    if response.status_code == 200:
      return response.json().get("elements", [])
    else:
      return []

  # プルダウンメニューの作成
  shop_dropdown = ft.Dropdown(
    options=[ft.dropdown.Option(key, value) for key, value in shop_types.items()],
    label="ショップの種類を選択",
    width=300,  # 幅を300pxに設定
    on_change=lambda e: on_shop_selected(e.control.value),
  )

  lv = ft.ListView(expand=True, spacing=10, auto_scroll=True)

  # ショップ情報を表示する関数
  def on_shop_selected(shop_type):
    lat, lon = 35.6895, 139.6917  # 東京都庁の緯度経度
    shops = fetch_shops(shop_type, lat, lon)
    lv.controls.clear()
    if shops:
      for shop in shops:
        lv.controls.append(
          ft.Text(f"ショップ名: {shop.get('tags', {}).get('name', '名前なし')}")
        )
    else:
      ft.Text("ショップが見つかりませんでした。")
    page.update()

  # 初期表示
  page.add(shop_dropdown)
  page.add(lv)


ft.app(target=main)
