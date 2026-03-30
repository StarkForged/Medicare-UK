from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display  = ['username', 'email', 'role', 'organisation', 'is_active']
    list_filter   = ['role', 'is_active']
    # Append our custom fields to the standard UserAdmin fieldsets
    fieldsets = UserAdmin.fieldsets + (
        ('Medicare UK', {'fields': ('role', 'organisation', 'phone', 'avatar')}),
    )
