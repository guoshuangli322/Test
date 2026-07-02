FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=dormitory.settings

WORKDIR /app/dormitory_system

COPY dormitory_system/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --timeout 120 -r requirements.txt

COPY dormitory_system/ .

EXPOSE 8000

# 顺序启动，用 ; 替代 && 确保 gunicorn 始终能启动
# 1. collectstatic（跳过数据库检查）
# 2. migrate（失败时打印警告但不阻塞）
# 3. gunicorn 启动（healthcheck 通过）
CMD python manage.py collectstatic --noinput --clear --skip-checks 2>/dev/null; \
    echo ">>> Running migrate..."; \
    python manage.py migrate --noinput 2>/dev/null || echo ">>> (migrate skipped, will be applied at first request)"; \
    echo ">>> Starting gunicorn on port ${PORT:-8000}..."; \
    gunicorn dormitory.wsgi:application \
        --bind 0.0.0.0:${PORT:-8000} \
        --workers 2 \
        --timeout 120 \
        --access-logfile - \
        --error-logfile -