STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
import os
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')