
## 11. Railway 云部署指南

### 11.1 前置准备

- [Railway 账户](https://railway.app/login)
- 项目代码推送到 GitHub

### 11.2 一键部署

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/新建模板)

**手动步骤**:

1. 登录 Railway → **New Project** → **Deploy from GitHub repo**
2. 选择仓库 → Railway 自动检测到 Dockerfile 并使用 Docker 构建（**不会**触发 Node.js 误检测）
3. 构建 + 部署约 3-5 分钟

### 11.3 添加 MySQL 数据库

1. 项目页面 → **+ New** → **Database** → **MySQL**
2. Railway 自动注入以下环境变量：
   - MYSQL_URL — 完整连接 URL（mysql://user:pass@host:port/dbname）
   - 或逐字段: MYSQL_HOST, MYSQL_PORT, MYSQL_DATABASE, MYSQL_USER, MYSQL_PASSWORD
3. Django 的 settings.py 会自动解析 MYSQL_URL 连接数据库

### 11.4 配置环境变量

在 Railway Dashboard → **Variables** 中添加：

| 变量 | 示例值 | 说明 |
|------|--------|------|
| DJANGO_SECRET_KEY | python -c "import secrets; print(secrets.token_urlsafe(50))" | 生产密钥，必填 |
| DJANGO_DEBUG | False | 生产环境必须设为 False |
| DJANGO_ALLOWED_HOSTS | .railway.app,你的域名.com | 允许访问的域名 |
| DJANGO_CSRF_TRUSTED_ORIGINS | https://*.railway.app | CSRF 白名单 |
| PORT | 8000 | Railway 自动分配，如需固定可手动设 |

### 11.5 初始化数据

部署成功后，进入 Railway Dashboard → **Shell** 执行：

`ash
python manage.py migrate --noinput
bash railway_init.sh
`

### 11.6 域名绑定

1. 项目设置 → **Domains** → **Generate Domain**
2. 获得 *.railway.app 域名
3. 更新 CSRF_TRUSTED_ORIGINS 变量为新域名

### 11.7 项目文件说明

| 文件 | 用途 |
|------|------|
| Dockerfile | **核心** — Docker 镜像构建（Python 3.11 + MySQL 客户端 + gunicorn） |
| ailway.json | Railway 配置（builder 设为 DOCKERFILE，跳过自动检测） |
| .dockerignore | 减小构建上下文，加速部署 |
| start.sh | 备用入口脚本（含 migrate + gunicorn 启动） |
| ailway_init.sh | 初始化脚本（创建管理员、示例账户、报修分类） |

### 11.8 常见问题

**Q: 仍然报 Cannot find module '/app/index.js'？**
A: 确认 ailway.json 的 uild.builder 为 DOCKERFILE，且 Dockerfile 存在于项目根目录。Railway 检测到 Dockerfile 后会完全跳过 Nixpacks。

**Q: mysqlclient 安装失败？**
A: Dockerfile 已包含 libmariadb-dev 等编译依赖。如失败，可检查构建日志确认 apt-get 阶段是否正常。

**Q: 数据库连接失败？**
A: 确认 MySQL Plugin 已创建并绑定到当前项目（Variables 中可见 MYSQL_URL）。首次创建后需等待约 30-60 秒。

**Q: 静态文件 404？**
A: Dockerfile 中已执行 collectstatic，使用 Whitenoise 提供服务。确认 whitenoise.middleware.WhiteNoiseMiddleware 在 MIDDLEWARE 中正确配置。

**Q: 如何查看日志？**
A: Railway Dashboard → **Deployments** → 选择部署 → **Logs**。
