from django.urls import path, include
from django.contrib import admin
from .views import storacha_health

urlpatterns = [
    path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),
    # ...other urls...
    path("storacha/health", storacha_health),
]