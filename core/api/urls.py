from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DocumentStampViewSet, health  # Only import what exists

router = DefaultRouter()
router.register(r"stamps", DocumentStampViewSet, basename="stamps")

urlpatterns = [
    path("", include(router.urls)),
    path("health/", health),
]