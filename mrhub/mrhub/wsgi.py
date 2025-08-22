import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mrhub.settings")

# Only start storacha token job if explicitly enabled
if os.getenv("STORACHA_ENABLED", "False").lower() == "true":
    try:
        from storacha_tokens import start_token_refresher  # noqa
        # start_token_refresher()   # call only if you really need it at boot
    except Exception as e:
        # Log and continue – don't block app boot in local dev
        print("Storacha not started:", e)

application = get_wsgi_application()