# 学生宿舍管理系统 — 本地部署教程

## 1. 环境要求

| 组件 | 版本 | 说明 |
|------|------|------|
| Python | >= 3.9 | 推荐 3.10+ |
| Django | 4.2.x | 已锁定 |
| MySQL | 8.0+ | 建议 8.0.28+ |
| pip | 最新版 | 包管理器 |

---

## 2. 数据库准备

### 2.1 安装 MySQL 8.0

Windows: 下载 MySQL Installer → 选择 MySQL Server 8.0 → 安装并设置 root 密码。

### 2.2 创建数据库

`sql
CREATE DATABASE IF NOT EXISTS dormitory_db
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;
`

或者直接执行项目根目录下的 db.sql：

`ash
mysql -u root -p < db.sql
`

---

## 3. Python 环境配置

`ash
cd dormitory_system
python -m venv venv
# Windows: .\venv\Scripts\Activate.ps1
pip install -r requirements.txt
`

> mysqlclient 安装失败？从 https://pypi.org/project/mysqlclient/#files 下载预编译 wheel。

---

## 4. 修改数据库配置

编辑 dormitory/settings.py 中的 DATABASES，修改 PASSWORD 为你的 MySQL 密码。

---

## 5. 初始化项目

`ash
python manage.py makemigrations accounts dorm student_mgr repair utility inspection announcement operation_log
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
python manage.py runserver 0.0.0.0:8000
`

访问 http://127.0.0.1:8000

---

## 6. 系统初始化流程

1. 超级管理员登录 → 用户管理创建宿管和学生账户
2. 添加楼栋 → 批量生成房间（自动创建床位）
3. 添加学生 → 办理入住
4. 其他功能按需使用

---

## 7. Railway 部署

### 7.1 部署步骤

1. 将代码推送到 GitHub
2. 登录 https://railway.app → New Project → Deploy from GitHub repo
3. Railway 自动检测 Dockerfile → Docker 构建（无需任何配置文件）
4. 添加 MySQL 数据库：+New → Database → MySQL
5. 设置环境变量（Variables）：
   - DJANGO_SECRET_KEY = 运行 python -c "import secrets; print(secrets.token_urlsafe(50))" 生成的密钥
   - DJANGO_DEBUG = False

### 7.2 初始化数据

部署成功后，在 Railway Dashboard → Shell 中执行：

`ash
python manage.py migrate --noinput
python manage.py createsuperuser
`

### 7.3 常见问题

**Dockerfile 构建失败**：确保 Dockerfile 的 CMD 使用 shell 格式（单行），不要用 exec 格式加 \ 续行。

**静态文件 404**：确认 settings.py 中 WhiteNoiseMiddleware 正确配置。

**MySQL 连接失败**：确认 MySQL Plugin 已创建并绑定到项目，MYSQL_URL 环境变量已注入。
