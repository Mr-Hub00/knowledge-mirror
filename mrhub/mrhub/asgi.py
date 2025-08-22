import os
from mrhub.storacha_tokens import start_token_refresher
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mrhub.settings')
start_token_refresher()
application = get_asgi_application()