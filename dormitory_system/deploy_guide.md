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

**Windows**: 下载 MySQL Installer → 选择 MySQL Server 8.0 → 安装并设置 root 密码。

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

> ⚠️ 注意：db.sql 包含完整建表语句 + 初始数据（管理员账户、报修分类）。
> Django ORM 也可自动建表（执行 migrate），但 db.sql 可供参考和手动初始化。

---

## 3. Python 环境配置

### 3.1 创建虚拟环境

`ash
# Windows (PowerShell)
cd dormitory_system
python -m venv venv
.\venv\Scripts\Activate.ps1

# 或 CMD
venv\Scripts\activate.bat
`

### 3.2 安装依赖

`ash
pip install -r requirements.txt
`

> mysqlclient 是 MySQL 的 Python 驱动，如果安装失败：
> - **Windows**: 下载预编译 wheel → https://pypi.org/project/mysqlclient/#files
> - 安装命令: pip install mysqlclient-*.whl

---

## 4. 修改数据库配置

编辑 dormitory/settings.py 中的 DATABASES 配置：

`python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dormitory_db',        # 数据库名
        'USER': 'root',                # MySQL 用户名
        'PASSWORD': '你的密码',         # MySQL 密码
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}
`

---

## 5. 初始化项目

`ash
# 进入项目目录
cd dormitory_system

# Django 数据库迁移（自动建表）
python manage.py makemigrations accounts dorm student_mgr repair utility inspection announcement operation_log
python manage.py migrate

# 创建超级管理员
python manage.py createsuperuser

# 创建静态文件目录
python manage.py collectstatic --noinput

# 启动开发服务器
python manage.py runserver 0.0.0.0:8000
`

访问: http://127.0.0.1:8000

---

## 6. 系统初始账户

| 角色 | 用户名 | 密码 | 说明 |
|------|--------|------|------|
| 超级管理员 | admin | admin123 | 全部权限 |
| 宿管 | manager1 | 123456 | 需手动创建 |
| 学生 | student1 | 123456 | 需手动创建 |

> 生产环境请务必修改默认密码！

---

## 7. 系统初始化流程

启动后建议按以下顺序录入数据：

1. **超级管理员登录** → 进入「用户管理」创建宿管和学生账户
2. **添加楼栋** → 宿舍管理 → 添加楼栋
3. **批量生成房间** → 选择楼栋 → 批量生成（自动创建房间+床位）
4. **添加学生** → 学生管理 → 添加学生（或 Excel 导入）
5. **办理入住** → 学生详情 → 办理入住
6. **其他功能** → 报修/水电/卫生检查/公告 按需使用

---

## 8. 项目结构

`
dormitory_system/
├── manage.py                 # Django 管理入口
├── requirements.txt          # Python 依赖
├── db.sql                    # MySQL 建表脚本（含初始数据）
├── deploy_guide.md           # 本部署教程
├── dormitory/                # 项目配置
│   ├── settings.py           # 全局配置
│   └── urls.py               # 主路由
├── apps/
│   ├── accounts/             # 用户认证模块
│   │   ├── models.py         # User 模型（三角色）
│   │   ├── views.py          # 登录/用户CRUD/仪表盘
│   │   └── forms.py          # 用户表单
│   ├── dorm/                 # 宿舍管理模块
│   │   ├── models.py         # Building/Room/Bed
│   │   └── views.py          # 楼栋/房间/床位/批量生成
│   ├── student_mgr/          # 学生管理模块
│   │   ├── models.py         # Student/DormitoryRecord
│   │   ├── views.py          # 入住/调宿/退宿/Excel导入导出
│   │   └── ajax_views.py     # AJAX接口（联动下拉框）
│   ├── repair/               # 报修工单模块
│   │   ├── models.py         # RepairOrder/RepairCategory
│   │   └── views.py          # 报修提交/处理/查询
│   ├── utility/              # 水电账单模块
│   │   ├── models.py         # UtilityBill
│   │   └── views.py          # 账单管理/缴纳/导出
│   ├── inspection/           # 卫生检查模块
│   │   └── views.py          # 检查记录/统计报表
│   ├── announcement/         # 公告模块
│   │   └── views.py          # 公告CRUD/浏览量
│   └── operation_log/        # 操作日志模块
│       ├── middleware.py      # 操作日志中间件（自动记录）
│       └── views.py           # 日志查看/导出
├── templates/                # 前端页面模板
│   ├── base.html             # 基础布局（侧边栏+顶部导航）
│   ├── dashboard.html        # 仪表盘（角色差异化展示）
│   └── accounts/ dorm/ student/ repair/ utility/ inspection/ announcement/ operation_log/
└── static/                   # 静态文件
`

---

## 9. 常见问题

### Q: mysqlclient 安装失败？
A: Windows 需要预编译 wheel 或安装 MySQL C Connector。推荐从 https://pypi.org/project/mysqlclient/#files 下载对应 Python 版本的 .whl 文件安装。

### Q: 页面样式加载异常？
A: 项目使用 BootCDN 加载 Bootstrap 5/FontAwesome，请确保网络通畅。或者下载到本地 static 目录。

### Q: 如何重置管理员密码？
A: python manage.py changepassword admin

### Q: 数据库迁移报错？
A: 确保 MySQL 已启动且 dormitory_db 数据库已创建。首次迁移建议 python manage.py migrate --run-syncdb。

---

## 10. 技术栈

- **后端**: Python 3.10+ / Django 4.2 LTS
- **数据库**: MySQL 8.0
- **前端**: Bootstrap 5 / FontAwesome 6 / jQuery 3
- **Excel处理**: openpyxl
- **身份认证**: Django Session Auth + 自定义角色系统
- **操作日志**: Django Middleware 自动拦截
- **三权分立**: 超级管理员 / 宿管 / 学生 各角色独立视图

---

## 11. Railway 云部署指南

Railway 是一个容器化部署平台，免费额度足够运行本系统。

### 11.1 前置准备

- [Railway 账户](https://railway.app/login)
- 项目代码推送到 GitHub（或从本地 CLI 上传）

### 11.2 一键部署（推荐）

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/新建模板)

或手动：

1. 登录 Railway → **New Project** → **Deploy from GitHub repo**
2. 选择你的仓库 → Railway 自动检测 ailway.json 并构建
3. 构建失败时，在项目 **Variables** 中添加以下环境变量：

| 变量 | 示例值 | 说明 |
|------|--------|------|
| DJANGO_SECRET_KEY | django-insecure-xxx... | 使用 python -c "import secrets; print(secrets.token_urlsafe(50))" 生成 |
| DJANGO_DEBUG | False | 生产环境务必设为 False |
| DJANGO_ALLOWED_HOSTS | .railway.app,你的域名 | 允许的主机 |
| DJANGO_CSRF_TRUSTED_ORIGINS | https://*.railway.app | CSRF 白名单 |

### 11.3 添加 MySQL 数据库

Railway 提供原生 MySQL 插件：

1. 在项目页面点击 **+ New** → **Database** → **MySQL**
2. Railway 自动注入以下环境变量到 Django 应用：
   - MYSQL_URL — 完整的连接 URL
   - 或逐字段: MYSQL_HOST, MYSQL_PORT, MYSQL_DATABASE, MYSQL_USER, MYSQL_PASSWORD
3. 系统会自动使用 MYSQL_URL 连接（见 settings.py 中的解析逻辑）

### 11.4 初始化数据（首次部署后）

在 Railway Dashboard 中打开项目，进入 **Shell** 标签页运行：

`ash
# 数据库迁移（如 release 阶段未自动执行）
python manage.py migrate --noinput

# 创建初始账户和分类数据
bash railway_init.sh
`

### 11.5 更新静态文件

Railway 每次部署会自动运行 collectstatic，静态文件通过 **Whitenoise** 直接提供服务，无需额外配置 CDN。

### 11.6 域名绑定（可选）

1. 项目设置 → **Domains** → **Generate Domain**
2. Railway 分配 *.railway.app 子域名
3. 更新 CSRF_TRUSTED_ORIGINS 变量为新域名
4. 可选绑定自定义域名

### 11.7 本地模拟 Railway 环境

`ash
# 使用 .env.example 中的环境变量启动
="True"
="mysql://root:123456@127.0.0.1:3306/dormitory_db"
python manage.py runserver
`

### 11.8 Railway 项目文件说明

| 文件 | 用途 |
|------|------|
| ailway.json | 主配置（构建命令、启动命令、健康检查） |
| Procfile | Heroku 兼容进程声明（release 阶段自动 migrate） |
| untime.txt | Python 版本锁定（3.11） |
| 
ixpacks.toml | Nixpacks 构建器备用配置（apt 依赖） |
| ailway_init.sh | 初始化脚本（创建管理员、报修分类、示例账户） |
| .env.example | 环境变量模板（本地开发/CI 参考） |

### 11.9 常见问题

**Q: 构建失败 — mysqlclient 编译错误？**
A: ailway.json 的 ptPackages 已包含 libmariadb-dev。如果仍然失败，在 Railway Dashboard → **Variables** 中添加 NIXPACKS_APT_PACKAGES=default-mysql-client build-essential python3-dev libmariadb-dev-compat libmariadb-dev pkg-config。

**Q: 数据库连接被拒绝？**
A: 确认 MySQL 插件已添加并绑定到应用（项目页面查看 **Variables** 是否有 MYSQL_URL）。MySQL 插件启动需要 30-60 秒。

**Q: 静态文件 404？**
A: 确认 whitenoise 在 INSTALLED_APPS 中排在 django.contrib.staticfiles 之前，且 MIDDLEWARE 中 WhiteNoiseMiddleware 紧跟在 SecurityMiddleware 之后。

**Q: 如何查看日志？**
A: Railway Dashboard → **Deployments** → 选择部署 → **Logs**。

**Q: 如何升级？**
A: 推送代码到 GitHub → Railway 自动重新构建部署。数据库迁移在 elease 阶段自动执行 python manage.py migrate。

### 11.10 常见部署错误

#### 错误: Cannot find module '/app/index.js'

**原因**: Railway 的 Nixpacks 自动检测将 Django 项目误识别为 Node.js，尝试启动 Node 运行时查找 index.js 入口。

**已在项目中做的修复（四层防护）**:

1. **nixpacks.toml** — providers = [\"python\"] 强制使用 Python 提供者
2. **railway.json** — 
ixpacksPlan 显式声明 Python 构建计划
3. **start.sh** — 入口脚本显式设置 DJANGO_SETTINGS_MODULE 后启动 gunicorn
4. **railwayignore** — 排除 .idea/ 等可能触发 Node.js 检测的文件

**应急方案**: 如果仍报错，在 Railway Dashboard > Variables 添加：

`
NIXPACKS_BUILDER = python
`

#### 错误: mysqlclient 编译失败

**原因**: MySQL C 客户端头文件缺失。已在 ailway.json 中预置 mysql_dev 等编译依赖。备选方案：

`
NIXPACKS_APT_PACKAGES = mysql_dev pkg-config openssl zlib gcc
`

#### 错误: DJANGO_SETTINGS_MODULE 未设置

**原因**: 环境变量未正确传递。start.sh 中已包含 export DJANGO_SETTINGS_MODULE=dormitory.settings 解决。
