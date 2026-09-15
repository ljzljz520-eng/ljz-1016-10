"""
楼宇系统运维后台 - Django 配置
开发环境配置；生产部署时请通过环境变量覆盖 SECRET_KEY / DEBUG 等。
"""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# 安全基础
# ---------------------------------------------------------------------------
SECRET_KEY = "django-insecure-dev-only-key-change-in-production"
DEBUG = True
ALLOWED_HOSTS = ["*"]

# ---------------------------------------------------------------------------
# 应用
# ---------------------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 业务应用（后续新模块在此追加）
    "apps.core",
    "apps.accounts",
    "apps.audit",
    "apps.dashboard",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# ---------------------------------------------------------------------------
# 数据库（默认 SQLite，后续可切换 PostgreSQL）
# ---------------------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ---------------------------------------------------------------------------
# 国际化
# ---------------------------------------------------------------------------
LANGUAGE_CODE = "zh-hans"
TIME_ZONE = "Asia/Shanghai"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ---------------------------------------------------------------------------
# 会话认证（前端通过 Vite 代理同源访问 /api，无需 CORS）
# ---------------------------------------------------------------------------
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_AGE = 60 * 60 * 8          # 会话有效期 8 小时
SESSION_SAVE_EVERY_REQUEST = True          # 活跃用户自动续期
CSRF_COOKIE_SAMESITE = "Lax"
# 生产环境（跨域部署前端时）需要配置：
# CSRF_TRUSTED_ORIGINS = ["https://your-frontend.example.com"]
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True

# ---------------------------------------------------------------------------
# 登录失败保护
# ---------------------------------------------------------------------------
LOGIN_FAILURE_LIMIT = 5                    # 窗口内允许的最大失败次数
LOGIN_FAILURE_WINDOW_MINUTES = 10          # 统计窗口（分钟）
LOGIN_LOCKOUT_MINUTES = 10                 # 锁定时长（分钟）
