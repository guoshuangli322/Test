# ================================================================
# Dockerfile — 学生宿舍管理系统
# 基础镜像: python:3.11-slim
# ================================================================

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=dormitory.settings

WORKDIR /app

# 安装 MySQL 编译依赖 + 清理缓存减小镜像体积
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc pkg-config libmariadb-dev libmariadb-dev-compat \
    && rm -rf /var/lib/apt/lists/*

# 安装 Python 依赖
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# 复制项目代码
COPY . .

# 收集静态文件
RUN python manage.py collectstatic --noinput --clear || true

EXPOSE 8000

# 重要: 使用 shell 格式（不用 exec 格式 + \ 续行）
CMD gunicorn dormitory.wsgi:application --bind 0.0.0.0:8000 --workers 2 --timeout 120 --access-logfile - --error-logfile -
