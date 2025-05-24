
from django.contrib import admin
from django.urls import path, include,re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView


schema_view = get_schema_view(
    openapi.Info(
        title="Cimo API",
        default_version='v1',
        description="API tài liệu cho hệ thống Cimo",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="support@cimo.vn"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('Users/', include('Users.urls')),
    path('Parents/', include('Parents.urls')),
    path('Students/',include('Students.urls')),
    path('ChatBot/', include('ChatBot.urls')),
    path('Auth/', include('Auth.urls')),
    path('blogs/',include('Blogs.urls')),
    # Swagger UI:
    path('schema/', SpectacularAPIView.as_view(), name='schema'),  # schema raw (json/yaml)
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
