from django.contrib import admin
from .models import Student, DormitoryRecord

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'real_name', 'gender', 'class_name', 'college', 'status')
    list_filter = ('status', 'gender', 'college')
    search_fields = ('student_id', 'real_name')

@admin.register(DormitoryRecord)
class DormitoryRecordAdmin(admin.ModelAdmin):
    list_display = ('student', 'bed', 'status', 'operation_type', 'checkin_date', 'operator')
    list_filter = ('status', 'operation_type')
