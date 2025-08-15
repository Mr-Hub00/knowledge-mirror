import os
from storacha_tokens import start_token_refresher
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mrhub.settings')
start_token_refresher()
application = get_wsgi_application()