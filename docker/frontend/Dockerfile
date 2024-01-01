FROM nginx:alpine

# 既存のデフォルト設定ファイルを削除
RUN rm /etc/nginx/conf.d/default.conf

# Nginx設定ファイルと静的ファイルをコピー
COPY nginx.conf /etc/nginx/conf.d
COPY index.html /var/www/index.html

# Nginxを前景で実行
CMD ["nginx", "-g", "daemon off;"]

# ポート80を公開
EXPOSE 80
