from django.contrib.auth import get_user_model
from rest_framework import viewsets
from .serializers import CustomUserSerializerPassword, CustomUserSerializerRead, CustomUserSerializerWrite, FollowSerializerList, FollowSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import ADMIN, CustomUser, Follow
from .mixins import ReadWriteSerializerMixin
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import action
from rest_framework import mixins

User = get_user_model()


class ListCreateViewSet(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    """
    Sends queryset or creates a model instance.
    """
    pass


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


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def delete_token(request):
    request.user.auth_token.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


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

    @action(
        detail=False,
        methods=['GET'],
    )
    def me(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=['POST'],
    )
    def set_password(self, request):
        new_password = request.data.get('new_password')
        current_password = request.data.get('current_password')
        user = CustomUser.objects.get(username=request.user.username)
        serializer = CustomUserSerializerPassword(
            data={'password': new_password})
        if check_password(current_password, user.password) and serializer.is_valid():
            user.password = make_password(new_password)
            user.save()
            return Response('Password had been changed', status=status.HTTP_200_OK)
        return Response('Please check the field current_password', status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=['GET'],
    )
    def subscriptions(self, request, pk=None):
        queryset = self.paginate_queryset(CustomUser.objects.filter(
            following__user=request.user))
        serializer = FollowSerializerList(
            queryset, many=True, context={
                'request': request
            }
        )
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
    )
    def subscribe(self, request, pk):
        if request.method == 'DELETE':
            subscription = get_object_or_404(
                Follow,
                following=get_object_or_404(CustomUser, id=pk),
                user=request.user
            )
            self.perform_destroy(subscription)
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer = FollowSerializer(
            data={
                'user': request.user.id,
                'following': get_object_or_404(CustomUser, id=pk).id
            },
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
