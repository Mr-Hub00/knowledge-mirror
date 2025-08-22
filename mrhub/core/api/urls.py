from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DocumentStampViewSet
from core.views import home, storacha_health, health

router = DefaultRouter()
router.register(r"stamps", DocumentStampViewSet, basename="stamps")

urlpatterns = [
    path("", include(router.urls)),              # mapping viewsets
    path("health/", health),                     # mapping the health view
]