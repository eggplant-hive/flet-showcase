# Pythonイメージをベースに使用
FROM python:3.12

# パッケージ更新
# RUN apt-get update

# 一般ユーザーを作成
RUN useradd -m fletuser

# デフォルトシェルをbashに設定
RUN chsh -s /bin/bash fletuser

# 作業ディレクトリを設定
WORKDIR /app

# 依存関係をインストールするため、requirements.txtをコピー
COPY requirements.txt ./

# 一般ユーザーに切り替える前にfletをインストールするためのディレクトリ権限を変更
RUN chown -R fletuser:fletuser /app

# 一般ユーザーに切り替え
USER fletuser

# 依存パッケージのインストール
RUN pip install --no-cache-dir --user -r requirements.txt

# アプリケーションのコードをコピー（appディレクトリの内容を全てコピー）
COPY app ./app/

# ~/.local/binをPATHに追加 (pipで--userオプションを使った場合のインストール先)
ENV PATH="/home/fletuser/.local/bin:$PATH"

# ポート指定（Fletのデフォルトポート）
EXPOSE 8550

# アプリケーションを起動
# Flet Webアプリケーションを実行するコマンド
CMD ["flet", "run", "--web", "main.py", "--port", "8550"]
