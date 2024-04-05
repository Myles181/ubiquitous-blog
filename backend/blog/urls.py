from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

scheme_view = get_schema_view(
    openapi.Info(
        title="Blog REST API",
        default_version="1.0.0",
        description="My Blog API Documentation"
    ),
    public=True,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include([
        path('', include('api.urls')),
        path('docs/', scheme_view.with_ui('swagger', cache_timeout=0)),
        ])),
]
