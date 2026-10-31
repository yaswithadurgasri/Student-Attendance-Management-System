from django.contrib import admin

from .models import (
    Department,
    Student,
    StaffMember,
    Attendance,
    Complaint
)

admin.site.register([
    Department,
    Student,
    StaffMember,
    Attendance,
    Complaint
])
