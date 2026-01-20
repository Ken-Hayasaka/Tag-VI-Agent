# Pythonのバージョン指定（基礎工事）
FROM python:3.10-slim

# 作業ディレクトリの作成
WORKDIR /app

# 資材をコピー
COPY . ./

# 必要な部品をインストール
RUN pip install --no-cache-dir -r requirements.txt

# ポート8080を開放（Google Cloud Runの標準規格）
EXPOSE 8080

# アプリ起動コマンド（ここが重要）
CMD streamlit run app.py --server.port 8080 --server.address 0.0.0.0
