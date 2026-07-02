# ================================================================
# Dockerfile — 学生宿舍管理系统
# 用途: Railway 部署（Dockerfile 存在时 Railway 跳过 Nixpacks）
# 基础镜像: python:3.11-slim（含 pip + 编译工具）
# ================================================================

FROM python:3.11-slim

# 环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    DJANGO_SETTINGS_MODULE=dormitory.settings

# 工作目录
WORKDIR /app

# ---- 1. 安装系统依赖（mysqlclient 编译所需） ----
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    pkg-config \
    libmariadb-dev \
    libmariadb-dev-compat \
    && rm -rf /var/lib/apt/lists/*

# ---- 2. 安装 Python 依赖 ----
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# ---- 3. 复制项目代码 ----
COPY . .

# ---- 4. 收集静态文件 ----
RUN python manage.py collectstatic --noinput --clear 2>/dev/null || true

# ---- 5. 暴露端口 & 启动 ----
EXPOSE 8000

CMD ["gunicorn", "dormitory.wsgi:application", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "2", \
     "--timeout", "120", \
     "--access-logfile", "-", \
     "--error-logfile", "-"]
