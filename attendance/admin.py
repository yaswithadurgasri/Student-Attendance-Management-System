from django.contrib import admin
from .models import Subject, Attendance


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('subject_code', 'subject_name')
    search_fields = ('subject_code', 'subject_name')


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'teacher', 'subject', 'date', 'status')
    list_filter = ('date', 'subject', 'teacher', 'status')
    search_fields = ('student__name', 'student__student_id')