from django.contrib import admin
from .models import UtilityBill

@admin.register(UtilityBill)
class UtilityBillAdmin(admin.ModelAdmin):
    list_display = ('room', 'year', 'month', 'utility_type', 'usage', 'amount', 'status')
    list_filter = ('status', 'utility_type', 'year', 'month')
    search_fields = ('room__room_number',)
