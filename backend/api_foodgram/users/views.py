from django.contrib.auth import get_user_model
from rest_framework import viewsets
from .serializers import CustomUserSerializerPassword, CustomUserSerializerRead, CustomUserSerializerWrite
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import ADMIN, CustomUser
from .mixins import ReadWriteSerializerMixin
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from django.contrib.auth.hashers import make_password


User = get_user_model()


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_token(request):
    email = request.data.get('email')
    password = request.data.get('password')
    if email is None or password is None:
        return Response('Data is invalid',
                        status=status.HTTP_400_BAD_REQUEST)
    user = get_object_or_404(User, email=email)
    if check_password(password, user.password):
        token = Token.objects.create(user=user)
        print(token)
        data = {
            'auth_token': str(token),
        }
        return Response(data, status.HTTP_201_CREATED)
    return Response('Data is invalid',
                    status=status.HTTP_400_BAD_REQUEST)


class DeleteToken(APIView):
    def post(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def change_password(request):
    new_password = request.data.get('new_password')
    current_password = request.data.get('current_password')
    user = CustomUser.objects.get(username=request.user.username)
    serializer = CustomUserSerializerPassword(
        data={'password': new_password})
    if check_password(current_password, user.password) and serializer.is_valid():
        user.password = make_password(new_password)
        user.save()
        return Response('Password changed', status=status.HTTP_200_OK)
    return Response('Please check current_password', status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(ReadWriteSerializerMixin, viewsets.ModelViewSet):
    queryset = User.objects.all()
    read_serializer_class = CustomUserSerializerRead
    write_serializer_class = CustomUserSerializerWrite

    def get_permissions(self):

        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def retrieve_me(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
