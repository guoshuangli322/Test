FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=dormitory.settings

WORKDIR /app

# 安装 Python 依赖
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --timeout 120 -r requirements.txt

# 复制代码
COPY . .

EXPOSE 8000

# 启动时按序执行: collectstatic → migrate → gunicorn
CMD python manage.py collectstatic --noinput --clear && \
    python manage.py migrate --noinput && \
    gunicorn dormitory.wsgi:application \
        --bind 0.0.0.0:${PORT:-8000} \
        --workers 2 \
        --timeout 120 \
        --access-logfile - \
        --error-logfile -
