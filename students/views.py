
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
    from django.shortcuts import get_object_or_404
from .models import StudentComplaint


@login_required
def student_complaint(request):

    student = get_object_or_404(
        StudentProfile,
        user=request.user,
        is_verified=True
    )

    if request.method == "POST":

        complaint_to = request.POST.get('complaint_to')
        subject = request.POST.get('subject')
        description = request.POST.get('description')

        if complaint_to not in ['staff', 'admin']:
            messages.error(request, "Invalid complaint recipient.")
            return redirect('student_complaint')

        if not subject or not description:
            messages.error(request, "Please fill all fields.")
            return redirect('student_complaint')

        StudentComplaint.objects.create(
            student=student,
            complaint_to=complaint_to,
            subject=subject,
            description=description
        )

        messages.success(request, "Complaint submitted successfully!")
        return redirect('student_dashboard')

    return render(
        request,
        'student_portal/complaint.html'
    )
