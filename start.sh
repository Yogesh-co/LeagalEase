#!/usr/bin/env bash
set -Eeuo pipefail

: "${PORT:=8080}"
export API_BASE_URL="${API_BASE_URL:-http://127.0.0.1:8001}"

envsubst '${PORT}' < /app/nginx/default.conf.template > /etc/nginx/conf.d/default.conf
nginx -t

uvicorn backend.main:app --host 0.0.0.0 --port 8001 &
api_pid=$!

streamlit run frontend/streamlit_app.py \
  --server.address 0.0.0.0 \
  --server.port 8501 \
  --server.headless true \
  --browser.gatherUsageStats false &
streamlit_pid=$!

nginx -g 'daemon off;' &
nginx_pid=$!

cleanup() {
  trap - EXIT INT TERM
  kill -TERM "$api_pid" "$streamlit_pid" "$nginx_pid" 2>/dev/null || true
  wait "$api_pid" "$streamlit_pid" "$nginx_pid" 2>/dev/null || true
}
trap cleanup EXIT INT TERM

wait -n "$api_pid" "$streamlit_pid" "$nginx_pid"
