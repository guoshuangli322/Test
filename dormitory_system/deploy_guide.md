# 学生宿舍管理系统 — 部署指南

## Railway 部署（推荐）

### 第一步: 创建 Railway 项目

**关键: 必须新建项目，不能复用旧项目。**

旧项目缓存了 Nixpacks 构建器配置，即使代码里有 Dockerfile 也会被忽略。

```bash
# 1. 代码推送到 GitHub
git add -A
git commit -m "ready for railway"
git push

# 2. 登录 Railway → 创建新项目
#    https://railway.app/new
#    选择 "Deploy from GitHub repo"
#    选择你的仓库 → Railway 自动检测 → 完成部署
```

### 第二步: 添加 MySQL

项目页面 → +New → Database → MySQL

### 第三步: 设置环境变量

Railway Dashboard → Variables:

| 变量 | 生成命令 / 值 |
|------|---------------|
| `DJANGO_SECRET_KEY` | `python -c "import secrets; print(secrets.token_urlsafe(50))"` |
| `DJANGO_DEBUG` | `False` |
| `DJANGO_ALLOWED_HOSTS` | `.railway.app` |

### 第四步: 初始化数据

Railway Dashboard → Shell:

```bash
python manage.py migrate --noinput
python manage.py createsuperuser
```

### 备用: 如果还是报 index.js 错误

在 Railway Dashboard → 项目 Settings → Builder:
- 手动切换为 **Dockerfile**
- 或创建一个 **全新的 Railway 项目**

### 本地开发

见上一步骤（Python venv + MySQL + migrate + runserver）。
