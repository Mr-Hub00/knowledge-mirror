from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
import os
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')