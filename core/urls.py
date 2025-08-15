from django.urls import path
from .views import storacha_health

urlpatterns = [
    # ...other routes...
    path("storacha/health", storacha_health),
]