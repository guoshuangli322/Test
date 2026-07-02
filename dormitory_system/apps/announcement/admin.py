from django.contrib import admin
from .models import Announcement

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'is_pinned', 'is_active', 'views', 'created_at')
    list_filter = ('category', 'is_pinned', 'is_active')
    search_fields = ('title',)
