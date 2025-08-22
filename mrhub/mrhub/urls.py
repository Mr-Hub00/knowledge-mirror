# iamhub/urls.py
from django.urls import path, include
from django.contrib import admin
from core.views import home, storacha_health, health
from core.views_public import public_stamp_view, public_stamp_pdf
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),
    path('api/v1/', include('core.api.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('s/<str:token>/', public_stamp_view, name='public-stamp'),
    path('s/<str:token>/receipt.pdf', public_stamp_pdf, name='public-stamp-pdf'),
    path('storacha/health', storacha_health),
    path("health/", health, name="health"),
    path("", home, name="home"),  # root URL
    path("favicon.ico", RedirectView.as_view(url="/static/favicon.ico", permanent=True)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += [path("health/", health)]