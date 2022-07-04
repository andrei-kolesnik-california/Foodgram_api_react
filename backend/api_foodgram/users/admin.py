from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


# class CustomUserAdmin(admin.ModelAdmin):
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'role', 'email')
    fieldsets = (
        ('User info', {'fields': ('username',
         'email', 'first_name', 'last_name', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'role')}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
