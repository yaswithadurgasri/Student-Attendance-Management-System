
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
from datetime import date
from .models import AttendanceCorrection


@login_required
def attendance_correction(request):

    student = get_object_or_404(
        StudentProfile,
        user=request.user,
        is_verified=True
    )

    if request.method == "POST":

        attendance_date = request.POST.get('attendance_date')
        subject = request.POST.get('subject', '').strip()
        reason = request.POST.get('reason', '').strip()

        try:
            selected_date = date.fromisoformat(attendance_date)

            if selected_date > date.today():
                messages.error(request, "Future dates are not allowed.")

            elif not subject or not reason:
                messages.error(request, "Please fill all fields.")

            else:
                AttendanceCorrection.objects.create(
                    student=student,
                    attendance_date=selected_date,
                    subject=subject,
                    reason=reason
                )

                messages.success(
                    request,
                    "Correction request submitted!"
                )

                return redirect('student_dashboard')

        except (ValueError, TypeError):
            messages.error(request, "Please enter a valid date.")

    return render(
        request,
        'student_portal/correction.html'
    )
