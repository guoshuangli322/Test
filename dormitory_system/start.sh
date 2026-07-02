#!/bin/bash
# ============================================================
# 启动脚本 — 用于 Railway Docker 部署
# Dockerfile 的 CMD 直接使用 gunicorn，此脚本保留作备用入口
# ============================================================
set -e

echo "[start.sh] 设置 DJANGO_SETTINGS_MODULE"
export DJANGO_SETTINGS_MODULE=dormitory.settings

echo "[start.sh] 数据库迁移..."
python manage.py migrate --noinput 2>/dev/null || true

echo "[start.sh] 启动 gunicorn..."
exec gunicorn dormitory.wsgi:application \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers ${GUNICORN_WORKERS:-2} \
    --timeout ${GUNICORN_TIMEOUT:-120} \
    --access-logfile - \
    --error-logfile - \
    --log-level ${GUNICORN_LOG_LEVEL:-info}
