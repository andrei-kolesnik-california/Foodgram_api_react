from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Tag, Ingredient, Recipe


class TagAdmin(ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug',)
    fieldsets = (
        ('Tags', {'fields': ('name', 'color', 'slug')}),
    )
    list_filter = ('name',)


admin.site.register(Tag, TagAdmin)


class IngredientAdmin(ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit',)
    fieldsets = (
        ('Ingredients', {'fields': ('name', 'measurement_unit')}),
    )
    list_filter = ('name',)


admin.site.register(Ingredient, IngredientAdmin)


class RecipeAdmin(ModelAdmin):
    list_display = ('id', 'get_tags', 'author', 'get_ingredients', 'is_favorited',
                    'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time')
    fieldsets = (
        ('Ingredients', {'fields': ('author', 'is_favorited',
                                    'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time')}),
    )
    list_filter = ('name',)


admin.site.register(Recipe, RecipeAdmin)
