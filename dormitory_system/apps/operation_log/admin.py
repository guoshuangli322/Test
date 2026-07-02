from django.contrib import admin
from .models import OperationLog

@admin.register(OperationLog)
class OperationLogAdmin(admin.ModelAdmin):
    list_display = ('username', 'action', 'module', 'ip_address', 'created_at')
    list_filter = ('module', 'created_at')
    search_fields = ('username', 'action')
