from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Tag


# class CustomUserAdmin(admin.ModelAdmin):
class TagAdmin(ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug',)
    fieldsets = (
        ('Tags', {'fields': ('name', 'color', 'slug')}),
    )
    list_filter = ('name',)


admin.site.register(Tag, TagAdmin)


# class CategoryAdmin(ModelAdmin):
#     list_display = ('id', 'name', 'slug')


# class CommentAdmin(ModelAdmin):
#     list_display = ('id', 'author', 'title', 'review', 'pub_date', 'text')
#     search_fields = ('text',)
#     list_filter = ('author', 'pub_date')
