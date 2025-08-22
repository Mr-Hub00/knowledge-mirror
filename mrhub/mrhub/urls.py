# iamhub/urls.py
from django.urls import path, include
from django.contrib import admin
from core.views import home, storacha_health, health
from core.views_public import public_stamp_view, public_stamp_pdf
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

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
]

# core/urls.py
from django.urls import path
from core.views import home, storacha_health, health

urlpatterns = [
    path("", home, name="home"),  # ensures "/" resolves cleanly
]

# mrhub/mrhub/core/views.py
def health(request):
    # Your health check logic here
    pass

# mrhub/urls.py
from django.contrib import admin
from django.urls import path, include
from core import views as core_views  # ensure this exists

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", core_views.index, name="home"),  # make sure core/views.py has index()
    path("api/", include("core.urls")),       # if you use DRF routes
]