from django.urls import path
from .views_healthz import healthz

urlpatterns = [
    # ...existing urls...
    path("healthz/", healthz, name="healthz"),
]