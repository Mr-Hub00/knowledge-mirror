INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'grappelli',  # Uncomment if using django-grappelli
    'championps',  # Your main app
]
ROOT_URLCONF = 'iamhub_project.urls'
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
import os
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')