from django.urls import path, include
from django.conf import settings
from django.contrib.staticfiles.urls import static
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

# Router para la API REST
router = DefaultRouter()
router.register('api/repuestos', views.RepuestoViewSet, basename='repuesto_api')

urlpatterns = [
    # Vistas web
    path('', views.inicio, name='inicio'),
    path('repuestos/', views.listado_repuestos, name='listado_repuestos'),
    path('crear/', views.crear_repuesto, name='crear_repuesto'),
    path('editar/<int:id>/', views.editar_repuesto, name='editar_repuesto'),
    path('eliminar/<int:id>/', views.eliminar_repuesto, name='eliminar_repuesto'),

    # Rutas API REST
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('api/auth/token/', obtain_auth_token, name='api_token_auth'),
    path('api/auth/jwt/', TokenObtainPairView.as_view(), name='jwt_obtain_pair'),
    path('api/auth/jwt/refresh/', TokenRefreshView.as_view(), name='jwt_refresh'),
    path('api/auth/registro/', views.RegistroUsuarioView.as_view(), name='api_registro'),

    # Rutas de vistas genéricas y de función
    path('api/generics/repuestos/', views.RepuestoListGenericView.as_view(), name='generics_list'),
    path('api/generics/repuestos/<int:pk>/', views.RepuestoDetailGenericView.as_view(), name='generics_detail'),
    path('api/fbv/repuestos/', views.repuesto_list_fbv, name='fbv_list'),
    path('api/fbv/repuestos/<int:pk>/', views.repuesto_detail_fbv, name='fbv_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
