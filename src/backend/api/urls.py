from rest_framework import routers
from django.urls import include, path

from .views import CustomUserViewSet, PostViewSet, RandomUserCreateViewSet

app_name = 'api'

router_v1 = routers.DefaultRouter()

router_v1.register('users', CustomUserViewSet, basename='users')
router_v1.register('posts', PostViewSet, basename='posts')
router_v1.register('random', RandomUserCreateViewSet, basename='random')


urlpatterns = [
    path('', include(router_v1.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
