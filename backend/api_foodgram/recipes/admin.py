from django.contrib import admin
from django.utils.html import format_html
from django.contrib.admin import ModelAdmin
from django.utils.safestring import mark_safe
from .models import Favorite, Purchase, Tag, Ingredient, Recipe, IngredientInRecipe


class IngredientInRecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'ingredient', 'amount')
    list_filter = ('recipe__name',)
    search_fields = ('recipe__name',)


admin.site.register(IngredientInRecipe, IngredientInRecipeAdmin)


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('id', 'name', 'slug', 'color', 'preview')
    list_filter = ('name',)
    search_fields = ('name',)

    def preview(self, obj):
        return format_html(
            f'<span style="color:{obj.color}; '
            f'width=20px; height=20px;">{obj.name}</span>'
        )


admin.site.register(Tag, TagAdmin)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


admin.site.register(Ingredient, IngredientAdmin)


class IngrediensInRecipeGet(admin.TabularInline):
    model = IngredientInRecipe


class RecipeAdmin(ModelAdmin):
    list_display = ('id', 'author', 'name', 'get_image', 'text',
                    'cooking_time', 'added_to_favorites_times',)
    fieldsets = (
        ('Ingredients', {'fields': ('author',
         'name', 'image', 'text', 'cooking_time')}),
    )
    list_filter = ('name', 'author', 'tags')

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="80" hieght="30"')

    def added_to_favorites_times(self, obj):
        return obj.favorite_recipe.count()


admin.site.register(Recipe, RecipeAdmin)


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    search_fields = ('user',)
    list_filter = ('user',)
    empty_value_display = '-пусто-'


admin.site.register(Favorite, FavoriteAdmin)


class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    list_filter = ('user', 'recipe')
    empty_value_display = '-пусто-'


admin.site.register(Purchase, PurchaseAdmin)
