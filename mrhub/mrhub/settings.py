# filepath: c:\Users\P\Desktop\IAMHUB\mrhub\mrhub\settings.py
import os
from pathlib import Path

from dotenv import load_dotenv

# -----------------------------------------------------------
# Paths & environment
# -----------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")  # loads if present; safe to keep for local dev

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mrhub.settings")

# Core toggles
DEBUG = os.getenv("DEBUG", "True") == "True"
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-only-not-for-prod")

# ALLOWED_HOSTS: always include your Fly domain, avoid duplicates/empties
allowed_hosts_env = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1")
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
if "mrhub.fly.dev" not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append("mrhub.fly.dev")

# CSRF_TRUSTED_ORIGINS: always include your Fly domain, avoid duplicates/empties
csrf_origins_env = os.getenv(
    "CSRF_TRUSTED_ORIGINS",
    "http://localhost,http://127.0.0.1,https://iamhub.net,https://*.onrender.com"
)
CSRF_TRUSTED_ORIGINS = [o.strip() for o in csrf_origins_env.split(",") if o.strip()]
if "https://mrhub.fly.dev" not in CSRF_TRUSTED_ORIGINS:
    CSRF_TRUSTED_ORIGINS.append("https://mrhub.fly.dev")

# -----------------------------------------------------------
# Installed apps
# -----------------------------------------------------------
INSTALLED_APPS = [
    "grappelli",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "core",
]

# -----------------------------------------------------------
# Middleware
# -----------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # WhiteNoise should be just after SecurityMiddleware
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "mrhub.urls"

# -----------------------------------------------------------
# Templates
# -----------------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "mrhub.wsgi.application"
ASGI_APPLICATION = "mrhub.asgi.application"

# -----------------------------------------------------------
# Database
# - SQLite for local dev
# - If DATABASE_URL is set (Render/Railway), it will override
# -----------------------------------------------------------
DATABASE_URL = os.getenv("DATABASE_URL", "")
if DATABASE_URL:
    # Requires: pip install dj-database-url
    import dj_database_url

    DATABASES = {
        "default": dj_database_url.parse(
            DATABASE_URL, conn_max_age=600, ssl_require=os.getenv("DB_SSL", "False") == "True"
        )
    }
else:
    import dj_database_url

    DATABASES = {
        "default": dj_database_url.config(default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}")
    }

# -----------------------------------------------------------
# Password validators (enable when you add real users)
# -----------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    # {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    # {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    # {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    # {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# -----------------------------------------------------------
# I18N / Timezone
# -----------------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = os.getenv("TIME_ZONE", "America/New_York")
USE_I18N = True
USE_TZ = True

# -----------------------------------------------------------
# Static & Media
# -----------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"
STORAGES = {"staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"}}

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# -----------------------------------------------------------
# Security (tighten automatically when DEBUG=False)
# -----------------------------------------------------------
if not DEBUG:
    SECURE_SSL_REDIRECT = False  # <-- set to False for Fly.io
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = int(os.getenv("SECURE_HSTS_SECONDS", "31536000"))  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_REFERRER_POLICY = "strict-origin"
    X_FRAME_OPTIONS = "DENY"
    CORS_ALLOW_ALL_ORIGINS = False
    CORS_ALLOWED_ORIGINS = ["https://mrhub.fly.dev"]
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
else:
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SECURE_SSL_REDIRECT = False   # Redirect HTTP to HTTPS in dev too

# -----------------------------------------------------------
# Logging (quiet in dev, informative in prod)
# -----------------------------------------------------------
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO" if not DEBUG else "WARNING")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "root": {"handlers": ["console"], "level": LOG_LEVEL},
}

# -----------------------------------------------------------
# Web3 / Storacha placeholders (read from .env when you wire them)
# -----------------------------------------------------------
ETH_RPC_URL = os.getenv("ETH_RPC_URL", "")
BCH_RPC_URL = os.getenv("BCH_RPC_URL", "")
STORACHA_API_KEY = os.getenv("STORACHA_API_KEY", "")
STORACHA_ENDPOINT = os.getenv("STORACHA_ENDPOINT", "")

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}

SITE_URL = "http://127.0.0.1:8000"
