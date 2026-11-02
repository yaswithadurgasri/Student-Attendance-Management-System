
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.db.models import Avg, Count, Q

from .models import (
    StaffProfile,
    Student,
    Attendance,
    PerformanceRemark,
    Complaint,
    Subject,
    TimetableEntry
)


def get_staff_profile(user):
    return get_object_or_404(
        StaffProfile,
        user=user,
        is_approved=True
    )


@login_required
def staff_dashboard(request):
    staff = get_staff_profile(request.user)

    if not staff.section:
        messages.warning(request, "Your section has not been assigned yet.")
        return render(request, "staff/staff_dashboard.html", {
            "staff": staff,
            "students": [],
            "subjects": staff.subjects.all(),
            "total_students": 0,
            "present_count": 0,
            "absent_count": 0,
            "average_attendance": 0,
        })

    students = Student.objects.filter(
        section=staff.section,
        department=staff.department,
        is_active=True
    )

    today = timezone.localdate()

    today_records = Attendance.objects.filter(
        student__in=students,
        date=today
    )

    present_count = today_records.filter(
        status="PRESENT"
    ).count()

    absent_count = today_records.filter(
        status="ABSENT"
    ).count()

    total_students = students.count()

    attendance_totals = Attendance.objects.filter(
        student__in=students
    ).values("student").annotate(
        total=Count("id"),
        present=Count("id", filter=Q(status="PRESENT"))
    )

    percentages = [
        (record["present"] / record["total"]) * 100
        for record in attendance_totals
        if record["total"] > 0
    ]

    average_attendance = (
        round(sum(percentages) / len(percentages), 2)
        if percentages else 0
    )

    student_data = []

    for student in students:
        student_today = today_records.filter(
            student=student
        ).first()

        student_data.append({
            "pk": student.pk,
            "name": student.name,
            "student_id": student.student_id,
            "today_status": (
                student_today.status if student_today else "NOT MARKED"
            ),
            "attendance_percentage": (
                round(
                    student.attendance_records.filter(
                        status="PRESENT"
                    ).count()
                    / student.attendance_records.count() * 100,
                    2
                )
                if student.attendance_records.exists() else 0
            ),
            "behaviour_remarks": (
                student.performance_records.order_by(
                    "-created_at"
                ).first().behaviour_remarks
                if student.performance_records.exists() else ""
            )
        })

    context = {
        "staff": staff,
        "students": student_data,
        "subjects": staff.subjects.all(),
        "total_students": total_students,
        "present_count": present_count,
        "absent_count": absent_count,
        "average_attendance": average_attendance,
    }

    return render(
        request,
        "staff/staff_dashboard.html",
        context
    )


@login_required
def staff_attendance_history(request):
    staff = get_staff_profile(request.user)

    records = Attendance.objects.filter(
        student__section=staff.section,
        student__department=staff.department
    ).select_related("student").order_by("-date")

    return render(request, "staff/attendance_history.html", {
        "staff": staff,
        "records": records
    })


@login_required
def staff_performance(request):
    staff = get_staff_profile(request.user)

    records = PerformanceRemark.objects.filter(
        student__section=staff.section,
        student__department=staff.department,
        staff=staff
    ).select_related("student", "subject")

    return render(request, "staff/performance.html", {
        "staff": staff,
        "records": records
    })


@login_required
def staff_timetable(request):
    staff = get_staff_profile(request.user)

    entries = TimetableEntry.objects.filter(
        staff=staff
    ).select_related("section", "subject").order_by(
        "day", "start_time"
    )

    return render(request, "staff/timetable.html", {
        "staff": staff,
        "entries": entries
    })


@login_required
def staff_complaints(request):
    staff = get_staff_profile(request.user)

    complaints = Complaint.objects.filter(
        target_teacher=staff,
        recipient="TEACHER"
    ).order_by("-created_at")

    return render(request, "staff/complaints.html", {
        "staff": staff,
        "complaints": complaints
    })


@login_required
def staff_complaint_history(request):
    staff = get_staff_profile(request.user)

    complaints = Complaint.objects.filter(
        submitted_by=request.user
    ).order_by("-created_at")

    return render(request, "staff/complaint_history.html", {
        "staff": staff,
        "complaints": complaints
    })


@login_required
def staff_reports(request):
    staff = get_staff_profile(request.user)

    students = Student.objects.filter(
        section=staff.section,
        department=staff.department,
        is_active=True
    )

    return render(request, "staff/reports.html", {
        "staff": staff,
        "students": students
    })


@login_required
def staff_settings(request):
    staff = get_staff_profile(request.user)

    return render(request, "staff/settings.html", {
        "staff": staff
    })
      
