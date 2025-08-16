# iamhub/urls.py
from django.urls import path, include
from django.contrib import admin
from core.views import home
from core.views_public import public_stamp_view, public_stamp_pdf
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from core.views import storacha_health

urlpatterns = [
    path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('api/v1/', include('core.api.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('s/<str:token>/', public_stamp_view, name='public-stamp'),
    path('s/<str:token>/receipt.pdf', public_stamp_pdf, name='public-stamp-pdf'),
    path('storacha/health', storacha_health),
]