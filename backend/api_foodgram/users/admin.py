from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Follow


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'role', 'first_name', 'last_name', 'email')
    fieldsets = (
        ('User info', {'fields': ('username',
         'email', 'first_name', 'last_name', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'role')}),
    )
    list_filter = ('username', 'email')


admin.site.register(User, CustomUserAdmin)

admin.site.register(Follow)
