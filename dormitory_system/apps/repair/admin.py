from django.contrib import admin
from .models import RepairCategory, RepairOrder

@admin.register(RepairCategory)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'sort_order')

@admin.register(RepairOrder)
class RepairOrderAdmin(admin.ModelAdmin):
    list_display = ('order_no', 'title', 'status', 'reporter', 'assignee', 'created_at')
    list_filter = ('status',)
    search_fields = ('order_no', 'title')
