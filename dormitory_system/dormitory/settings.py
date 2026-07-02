import os
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# =========================================================================
# Railway 环境适配
# =========================================================================
# Railway 会提供以下环境变量（MySQL Plugin）：
#   MYSQL_URL      -> mysql://user:pass@host:port/dbname
#   或者逐字段:
#   MYSQL_HOST, MYSQL_PORT, MYSQL_DATABASE, MYSQL_USER, MYSQL_PASSWORD
#
# 本地开发回退到 dormitory_db / root / 123456
# =========================================================================

def parse_mysql_url(url):
    """解析 MYSQL_URL 为 Django DATABASES 字典"""
    # mysql://user:password@host:port/database
    pattern = r'mysql://([^:]+):([^@]+)@([^:]+):(\d+)/(.+)'
    m = re.match(pattern, url)
    if m:
        return {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': m.group(5),
            'USER': m.group(1),
            'PASSWORD': m.group(2),
            'HOST': m.group(3),
            'PORT': m.group(4),
            'OPTIONS': {
                'charset': 'utf8mb4',
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            },
        }
    return None


# ---------- SECRET KEY ----------
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'django-insecure-dev-key-do-not-use-in-production'
)

# ---------- DEBUG ----------
DEBUG = os.environ.get('DJANGO_DEBUG', 'False').lower() in ('true', '1', 'yes')

# ---------- ALLOWED HOSTS ----------
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '127.0.0.1,localhost,.railway.app').split(',')

# ---------- CSRF Trusted Origins ----------
CSRF_TRUSTED_ORIGINS = os.environ.get(
    'DJANGO_CSRF_TRUSTED_ORIGINS',
    'http://127.0.0.1:8000,http://localhost:8000'
).split(',')

# ---------- DATABASE ----------
# 优先级: MYSQL_URL > 逐字段环境变量 > 本地回退
MYSQL_URL = os.environ.get('MYSQL_URL', '')
if MYSQL_URL:
    db_config = parse_mysql_url(MYSQL_URL)
    DATABASES = {'default': db_config} if db_config else {}
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ.get('MYSQL_DATABASE', 'dormitory_db'),
            'USER': os.environ.get('MYSQL_USER', 'root'),
            'PASSWORD': os.environ.get('MYSQL_PASSWORD', '123456'),
            'HOST': os.environ.get('MYSQL_HOST', '127.0.0.1'),
            'PORT': os.environ.get('MYSQL_PORT', '3306'),
            'OPTIONS': {
                'charset': 'utf8mb4',
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            },
        }
    }

# =========================================================================
# 应用 & 中间件
# =========================================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 第三方
    'whitenoise.runserver_nostatic',  # 开发环境也使用 whitenoise
    # 自定义应用
    'apps.accounts',
    'apps.dorm',
    'apps.student_mgr',
    'apps.repair',
    'apps.utility',
    'apps.inspection',
    'apps.announcement',
    'apps.operation_log',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # 静态文件服务（生产环境关键）
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 操作日志（拦截 POST/PUT/DELETE）
    'apps.operation_log.middleware.OperationLogMiddleware',
]

ROOT_URLCONF = 'dormitory.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.accounts.context_processors.current_user',
            ],
        },
    },
]

WSGI_APPLICATION = 'dormitory.wsgi.application'

# =========================================================================
# 密码 & 国际化
# =========================================================================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
]

LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_TZ = True

# =========================================================================
# 静态文件 — Whitenoise（无需 Nginx）
# =========================================================================

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'static_root'

# Whitenoise 压缩 & 永久缓存（生产环境）
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# =========================================================================
# 媒体文件（上传）
# =========================================================================

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# =========================================================================
# Django 默认配置
# =========================================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'accounts.User'
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/accounts/login/'
PAGE_SIZE = 15

# =========================================================================
# 日志（Railway 容器日志）
# =========================================================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{asctime}] {levelname} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': os.environ.get('DJANGO_LOG_LEVEL', 'INFO'),
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.environ.get('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
    },
}
