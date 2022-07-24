from django_filters.rest_framework.filterset import FilterSet
from django_filters import filters
from django.contrib.auth import get_user_model
from django_filters.rest_framework import FilterSet, filters
from rest_framework.filters import SearchFilter

from .models import Recipe

User = get_user_model()

latin_to_cyrillic = str.maketrans(
    'qwertyuiop[]asdfghjkl;\'zxcvbnm,./',
    'йцукенгшщзхъфывапролджэячсмитьбю.'
)

filter_choices = {
    'is_favorited': 'favorite_recipe',
    'is_in_shopping_cart': 'purchase',
}


class IngredientSearchFilter(SearchFilter):
    search_param = 'name'


class RecipeFilter(FilterSet):
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')
    is_favorited = filters.BooleanFilter(method='get_boolean')
    is_in_shopping_cart = filters.BooleanFilter(
        method='get_boolean'
    )

    def get_boolean(self, queryset, name, value):
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(**{f'{filter_choices[name]}__user': self.request.user})
        return queryset

    class Meta:
        model = Recipe
        fields = ['tags', 'author', 'is_favorited', 'is_in_shopping_cart']
