#!/bin/bash
# ============================================================
# Railway 启动脚本
# 显式设置 Django 配置模块后启动 gunicorn
# ============================================================
set -e

echo "[start.sh] 设置 DJANGO_SETTINGS_MODULE=dormitory.settings"
export DJANGO_SETTINGS_MODULE=dormitory.settings

echo "[start.sh] 收集静态文件..."
python manage.py collectstatic --noinput --clear 2>/dev/null || true

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
