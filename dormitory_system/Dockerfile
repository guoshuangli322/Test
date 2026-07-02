FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=dormitory.settings

WORKDIR /app

# 编译 mysqlclient 所需系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc pkg-config libmariadb-dev libmariadb-dev-compat \
    && rm -rf /var/lib/apt/lists/*

# 安装 Python 依赖
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput --clear || true

EXPOSE 8000

# shell 格式，无反斜杠续行
CMD gunicorn dormitory.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 2 --timeout 120 --access-logfile - --error-logfile -
