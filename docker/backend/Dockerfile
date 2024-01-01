# 使用するPythonのバージョン
FROM python:3.9

WORKDIR /app

# 必要なファイルのみコピー
COPY requirements.txt .
COPY server.py .

# 依存関係のインストール
RUN pip install --no-cache-dir -r requirements.txt

# コンテナ起動時にサーバーを実行
CMD ["python", "server.py"]
