from django.urls import path
from django.views.generic import RedirectView
from core.views import home, storacha_health, health

urlpatterns = [
    path("", home, name="home"),
    path("storacha/health", storacha_health),
    path("health/", health, name="health"),
    path("favicon.ico", RedirectView.as_view(url="/static/favicon.ico", permanent=True)),
]