from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation for TestTask",
        default_version="v1",
        description="API documentation",
        license=openapi.License(name="BSD License"),
    ),
    patterns=[
        path("api/", include("api.urls")),
    ],
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = (
    path("admin/", admin.site.urls),
    path("api/", include("api.urls", namespace="api")),
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
)

if settings.DEBUG:
    urlpatterns += tuple(
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    )