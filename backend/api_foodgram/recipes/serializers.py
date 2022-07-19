from django.contrib.auth import get_user_model
from drf_base64.fields import Base64ImageField
from rest_framework import serializers
from users.serializers import CustomUserSerializerRead
from .models import Tag, Ingredient, Recipe, IngredientInRecipe, Favorite, Purchase

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug', 'color')
        read_only_fields = ('id', 'name', 'slug', 'color')


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientInRecipeGetSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(source='ingredient'
                                                 '.measurement_unit')

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(read_only=True, many=True,)
    author = CustomUserSerializerRead(read_only=True)
    ingredients = IngredientInRecipeGetSerializer(many=True,
                                                  read_only=True,
                                                  source='ingredient_amount')
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart',
                  'name', 'image', 'text', 'cooking_time')

    def get_is_favorited(self, obj):
        return self.boolen_request(obj, Favorite)

    def get_is_in_shopping_cart(self, obj):
        return self.boolen_request(obj, Purchase)

    def boolen_request(self, request_obj, main_obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return main_obj.objects.filter(user=request.user,
                                       recipe=request_obj.id).exists()

    def validate(self, data):
        # author = self.context.get('request').user
        ingredients = self.initial_data.get('ingredients')
        tags = self.initial_data.get('tags')

        for ingredient in ingredients:
            amount = ingredient.get('amount')
            try:
                int(amount)
            except ValueError:
                raise serializers.ValidationError(
                    'Ingredient amount must be a number'
                )
            if int(amount) < 1:
                raise serializers.ValidationError(
                    'Please input a number not less than one'
                )
        data['ingredients'] = ingredients
        data['tags'] = tags
        # data['author'] = author
        return data

    @staticmethod
    def create_ingredients_tags(recipe, ingredients, tags):
        for ingredient in ingredients:
            IngredientInRecipe.objects.create(
                recipe=recipe,
                ingredient_id=ingredient['id'],
                amount=ingredient['amount']
            )
        for tag in tags:
            recipe.tags.add(tag)

    def create(self, validated_data):
        image = validated_data.pop('image')
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(
            image=image,
            **validated_data
        )
        self.create_ingredients_tags(recipe, ingredients, tags)
        return recipe

    def update(self, recipe, validated_data):
        recipe.tags.clear()
        IngredientInRecipe.objects.filter(recipe=recipe).delete()
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        self.create_ingredients_tags(recipe, ingredients, tags)
        return super().update(recipe, validated_data)


class RecipeShowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FavoriteRecipesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ('user', 'recipe')

    def validate(self, data):
        if Favorite.objects.filter(
                user=self.context.get('request').user,
                recipe=data['recipe']
        ).exists():
            raise serializers.ValidationError({
                'status': 'Already added'
            })
        return data

    def to_representation(self, instance):
        return RecipeShowSerializer(
            instance.recipe,
            context={'request': self.context.get('request')}
        ).data


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ('user', 'recipe')

    def validate(self, data):
        if Purchase.objects.filter(
                user=self.context['request'].user,
                recipe=data['recipe']
        ):
            raise serializers.ValidationError('Already added')
        return data

    def to_representation(self, instance):
        return RecipeShowSerializer(
            instance.recipe,
            context={'request': self.context.get('request')}
        ).data
