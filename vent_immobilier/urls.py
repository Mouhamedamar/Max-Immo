from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.schemas import get_schema_view
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # ---------------------------
    # Admin Django
    # ---------------------------
    path('admin/', admin.site.urls),

   

    # ---------------------------
    # API principale (max_app)
    # ---------------------------
    path('api/', include('max_app.urls')),


    # ---------------------------
    # Authentification Token DRF
    # ---------------------------
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),

    # ---------------------------
    # Authentification session (interface DRF)
    # ---------------------------
    path('api-auth/', include('rest_framework.urls')),

    # ---------------------------
    # Documentation OpenAPI/Swagger
    # ---------------------------
    path(
        'openapi/',
        get_schema_view(
            title="Vent Immobilier API",
            description="Documentation interactive pour toutes les routes de l'API",
            version="1.0.0"
        ),
        name='openapi-schema'
    ),
    path(
        'docs/',
        TemplateView.as_view(
            template_name='documentation.html',
            extra_context={'schema_url': 'openapi-schema'}
        ),
        name='swagger-ui'
    ),
]

# ---------------------------
# Gestion des fichiers médias
# ---------------------------
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
