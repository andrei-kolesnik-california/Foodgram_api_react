from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import CustomUser
from rest_framework.validators import UniqueTogetherValidator


class CustomUserSerializerRead(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', "is_subscribed",)


class CustomUserSerializerWrite(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'first_name',
                  'last_name', "password")

        validators = [
            UniqueTogetherValidator(
                queryset=CustomUser.objects.all(),
                fields=('email', 'username', )
            )
        ]

    def create(self, validated_data):
        user = CustomUser(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        password = validated_data['password']
        user.password = make_password(password)
        user.save()
        user.password = password
        return user

    # def create(self, validated_data):
    #     validated_data['password'] = make_password(
    #         validated_data.get('password'))
    #     return super(CustomUserSerializerWrite, self).create(validated_data)


class CustomUserSerializerPassword(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('password',)
