import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-default-key")
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

def env_list(name: str):
    raw = os.getenv(name, "")
    return [item.strip() for item in raw.split(",") if item.strip()]

ALLOWED_HOSTS = env_list("ALLOWED_HOSTS")
CSRF_TRUSTED_ORIGINS = env_list("CSRF_TRUSTED_ORIGINS")

# Safety net: pick up the Render hostname automatically
RENDER_HOST = os.getenv("RENDER_EXTERNAL_HOSTNAME")
if RENDER_HOST:
    if RENDER_HOST not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(RENDER_HOST)
    if ".onrender.com" not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(".onrender.com")
    render_origin = f"https://{RENDER_HOST}"
    if render_origin not in CSRF_TRUSTED_ORIGINS:
        CSRF_TRUSTED_ORIGINS.append(render_origin)

# Local dev safety fallback
if DEBUG and not ALLOWED_HOSTS:
    ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
if DEBUG and not CSRF_TRUSTED_ORIGINS:
    CSRF_TRUSTED_ORIGINS = ["http://127.0.0.1:8000", "http://localhost:8000"]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 25,
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024

INSTALLED_APPS = [
    'grappelli',
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "drf_spectacular",
    "corsheaders",
    "core",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  # <-- moved above CSRF
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Storacha feature flag and config
STORACHA_ENABLED = os.getenv("STORACHA_ENABLED", "False").lower() == "true"
STORACHA_ENDPOINT = os.getenv("STORACHA_ENDPOINT", "")
STORACHA_API_KEY = os.getenv("STORACHA_API_KEY", "")

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"
    }
}

SPECTACULAR_SETTINGS = {
    "TITLE": "IAmHub API",
    "DESCRIPTION": "Decentralized sovereignty hub APIs",
    "VERSION": "1.0.0",
}

# --- Shareable stamp links (stateless, HMAC) ---
FEATURE_SHARE_STAMP = os.getenv("FEATURE_SHARE_STAMP", "True").lower() == "true"
SHARELINK_TTL_SECONDS = 60 * 60       # 1 hour TTL

# --- Email basics ---
EMAIL_BACKEND = os.getenv("EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "no-reply@iamhub.net")
SITE_URL = os.getenv("SITE_URL", "http://127.0.0.1:8000")
ADMINS_EMAIL = os.getenv("ADMINS_EMAIL", "")

ADMINS = [("Admin", os.getenv("ADMINS_EMAIL", ""))] if os.getenv("ADMINS_EMAIL") else []

# receipts
FEATURE_EMAIL_RECEIPTS = os.getenv("FEATURE_EMAIL_RECEIPTS", "True").lower() == "true"
FEATURE_VERIFICATION_EMAILS = True

INTERNAL_CRON_TOKEN = os.getenv("INTERNAL_CRON_TOKEN", "")

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

SECURE_HSTS_SECONDS = int(os.getenv("SECURE_HSTS_SECONDS", "60"))
SECURE_HSTS_INCLUDE_SUBDOMAINS = os.getenv("SECURE_HSTS_INCLUDE_SUBDOMAINS", "True").lower() == "true"
SECURE_HSTS_PRELOAD = os.getenv("SECURE_HSTS_PRELOAD", "False").lower() == "true"
SECURE_SSL_REDIRECT = os.getenv("SECURE_SSL_REDIRECT", "True").lower() == "true"
SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "True").lower() == "true"
CSRF_COOKIE_SECURE = os.getenv("CSRF_COOKIE_SECURE", "True").lower() == "true"
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# CORS settings
CORS_ALLOW_ALL_ORIGINS = True  # Change this in production!
CORS_ALLOW_CREDENTIALS = True

if not DEBUG:
    CORS_ALLOW_ALL_ORIGINS = False
    CORS_ALLOWED_ORIGINS = [
        "https://iamhub-fresh-b0gi.onrender.com",
        "https://iamhub.net",
        "https://www.iamhub.net",
    ]
    # Optionally auto-add the Render origin to CORS in prod
    if RENDER_HOST:
        ro = f"https://{RENDER_HOST}"
        if ro not in CORS_ALLOWED_ORIGINS:
            CORS_ALLOWED_ORIGINS.append(ro)

if DEBUG:
    print("ALLOWED_HOSTS:", ALLOWED_HOSTS)
    print("CSRF_TRUSTED_ORIGINS:", CSRF_TRUSTED_ORIGINS)