"""
URL configuration for bancoSangre project.

The urlpatterns list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
"""
from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from donador.api.views_mapa import donadores_para_mapa
from usuario.api.views import UsuarioViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


router = DefaultRouter()
router.register('usuarios', UsuarioViewSet, basename='usuario')


urlpatterns = [
    # Servir React app en la raíz y para rutas no API/admin
    path('', never_cache(TemplateView.as_view(template_name="index.html")), name='react-app'),

    # API y admin routes
    path('api/mapa/donadores/', donadores_para_mapa),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/', include('usuario.api.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/rol/', include('rol.api.urls')),
    path('api/municipio/', include('municipio.api.urls')),
    path('api/colonia/', include('colonia.api.urls')),
    path('api/coordenada/', include('coordenada.api.urls')),
    path('api/direccion/', include('direccion.api.urls')),
    path('api/donador/', include('donador.api.urls')),
    path('api/cita/', include('cita.api.urls')),

    # Catch-all para que React maneje rutas del frontend que no sean API o admin
    path('<path:path>', never_cache(TemplateView.as_view(template_name="index.html")), name='react-app-catchall'),
]
