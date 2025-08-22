import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mrhub.settings")

try:
    if os.getenv("STORACHA_ENABLED", "False").lower() == "true":
        from storacha_tokens import start_token_refresher
        start_token_refresher()
except Exception:
    pass

application = get_wsgi_application()