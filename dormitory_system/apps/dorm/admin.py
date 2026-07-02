from django.contrib import admin
from .models import Building, Room, Bed

@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'floors', 'gender_type', 'manager', 'is_active')
    list_filter = ('gender_type', 'is_active')

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('building', 'room_number', 'room_type', 'floor', 'bed_count', 'is_active')
    list_filter = ('building', 'room_type')

@admin.register(Bed)
class BedAdmin(admin.ModelAdmin):
    list_display = ('room', 'bed_number', 'status')
    list_filter = ('status',)
