from django.urls import path
from core.views import home, storacha_health, health

urlpatterns = [
    path("", home, name="home"),
    path("storacha/health", storacha_health),
    path("health/", health, name="health"),
]