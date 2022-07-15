from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, get_token, delete_token

app_name = 'users'

router = DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('auth/token/login/', get_token, name='get_token'),
    path('auth/token/logout/', delete_token, name='delete_token'),
    # path('users/set_password/', change_password, name='change_password'),
    path('', include(router.urls)),
]
