
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def student_dashboard(request):

    student = request.user

    # Replace these sample values with database records
    attendance_percentage = 85
    present_count = 85
    absent_count = 15
    performance = 90

    attendance_records = []
    marks = []

    context = {
        'student': student,
        'attendance_percentage': attendance_percentage,
        'present_count': present_count,
        'absent_count': absent_count,
        'performance': performance,
        'attendance_records': attendance_records,
        'marks': marks,
    }

    return render(
        request,
        'student_portal/dashboard.html',
        context
    )
