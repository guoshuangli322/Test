from django.contrib import admin
from .models import HygieneInspection

@admin.register(HygieneInspection)
class InspectionAdmin(admin.ModelAdmin):
    list_display = ('room', 'score', 'grade', 'inspector', 'check_date')
    list_filter = ('grade', 'check_date')
