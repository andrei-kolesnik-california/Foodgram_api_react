from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, get_token, DeleteToken, change_password

app_name = 'users'

router = DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('auth/token/login/', get_token, name='get_token'),
    path('auth/token/logout/', DeleteToken.as_view(), name='delete_token'),
    path('users/set_password/', change_password, name='change_password'),
    path('users/me/',
         UserViewSet.as_view(({'get': 'retrieve_me'}))),
    path('', include(router.urls)),
]
