from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'name', 'section')
    search_fields = ('student_id', 'name')
    list_filter = ('section',)