from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'real_name', 'role', 'phone', 'email', 'is_active')
    list_filter = ('role', 'is_active')
    search_fields = ('username', 'real_name', 'phone')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('个人信息', {'fields': ('real_name', 'phone', 'email', 'avatar')}),
        ('角色权限', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups')}),
        ('时间信息', {'fields': ('last_login', 'date_joined')}),
    )
