from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import FoodgramUser, Follow
from recipes.models import Recipe
from rest_framework.validators import UniqueTogetherValidator
from django.shortcuts import get_object_or_404


class FoodgramUserSerializerRead(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = FoodgramUser
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', "is_subscribed",)

    def get_is_subscribed(self, following):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(
            user=user,
            following=following
        ).exists()


class FoodgramUserSerializerWrite(serializers.ModelSerializer):

    class Meta:
        model = FoodgramUser
        fields = ('email', 'username', 'first_name',
                  'last_name', "password")

        validators = [
            UniqueTogetherValidator(
                queryset=FoodgramUser.objects.all(),
                fields=('email', 'username', )
            )
        ]

    def create(self, validated_data):
        user = FoodgramUser(
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


class FoodgramUserSerializerPassword(serializers.ModelSerializer):

    class Meta:
        model = FoodgramUser
        fields = ('password',)


class FollowSerializerList(serializers.ModelSerializer):
    """ Сериализация списка при GET запросе"""
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = FoodgramUser
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count'
        )

    def get_recipes_count(self, following):
        return Recipe.objects.filter(author=following).count()

    def get_recipes(self, following):
        queryset = self.context.get('request')
        return RecipeFollowingSerializer(
            Recipe.objects.filter(author=following),
            many=True, context={'request': queryset}
        ).data

    def get_is_subscribed(self, following):
        return Follow.objects.filter(
            user=self.context.get('request').user,
            following=following
        ).exists()


class RecipeFollowingSerializer(serializers.ModelSerializer):
    """ Сериализация списка рецептов """
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FollowSerializer(serializers.ModelSerializer):
    """ Сериализация при подписке """
    class Meta:
        model = Follow
        fields = ('user', 'following')

    def validate(self, data):
        get_object_or_404(FoodgramUser, username=data['following'])
        if self.context['request'].user == data['following']:
            raise serializers.ValidationError(
                'You can not subscribe by yourself')
        if Follow.objects.filter(
                user=self.context['request'].user,
                following=data['following']
        ):
            raise serializers.ValidationError('Subscribtion is already exists')
        return data

    def to_representation(self, instance):
        return FollowSerializerList(
            instance.following,
            context={'request': self.context.get('request')}
        ).data
