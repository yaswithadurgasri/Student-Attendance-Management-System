
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.db.models import Avg, Count, Q

from .models import (
    StaffProfile,
    Department,
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


from django import forms
from django.shortcuts import get_object_or_404
from django.urls import reverse


class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = [
            "student_id",
            "name",
            "department",
            "section",
            "academic_year",
            "email",
            "phone",
            "is_active",
        ]


def get_assigned_students(staff):
    return Student.objects.filter(
        department=staff.department,
        section=staff.section
    )


@login_required
def staff_student_add(request):
    staff = get_staff_profile(request.user)

    if request.method == "POST":
        form = StudentForm(request.POST)

        if form.is_valid():
            student = form.save(commit=False)

            # Staff can add students only to their assigned section.
            student.department = staff.department
            student.section = staff.section
            student.academic_year = staff.academic_year
            student.save()

            messages.success(request, "Student added successfully!")
            return redirect("staff:dashboard")
    else:
        form = StudentForm()

    form.fields["department"].queryset = (
        type(staff.department).objects.filter(pk=staff.department_id)
        if staff.department_id else type(staff.department).objects.none()
    )

    form.fields["section"].queryset = (
        type(staff.section).objects.filter(pk=staff.section_id)
        if staff.section_id else type(staff.section).objects.none()
    )

    return render(request, "staff/student_form.html", {
        "form": form,
        "staff": staff,
        "page_title": "Add Student"
    })


@login_required
def staff_student_edit(request, student_id):
    staff = get_staff_profile(request.user)

    student = get_object_or_404(
        get_assigned_students(staff),
        pk=student_id
    )

    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)

        if form.is_valid():
            updated_student = form.save(commit=False)

            # Prevent moving a student outside assigned section.
            updated_student.department = staff.department
            updated_student.section = staff.section
            updated_student.academic_year = staff.academic_year
            updated_student.save()

            messages.success(request, "Student updated successfully!")
            return redirect("staff:dashboard")
    else:
        form = StudentForm(instance=student)

    form.fields["department"].queryset = Department.objects.filter(
        pk=staff.department_id
    )
    form.fields["section"].queryset = Section.objects.filter(
        pk=staff.section_id
    )

    return render(request, "staff/student_form.html", {
        "form": form,
        "staff": staff,
        "page_title": "Edit Student"
    })


@login_required
@require_POST
def staff_student_delete(request, student_id):
    staff = get_staff_profile(request.user)

    student = get_object_or_404(
        get_assigned_students(staff),
        pk=student_id
    )

    student.delete()

    messages.success(request, "Student deleted successfully!")
    return redirect("staff:dashboard")


@login_required
def staff_student_search(request):
    staff = get_staff_profile(request.user)

    query = request.GET.get("q", "").strip()

    students = get_assigned_students(staff).filter(
        Q(name__icontains=query) |
        Q(student_id__icontains=query)
    ) if query else get_assigned_students(staff)

    return render(request, "staff/student_search.html", {
        "staff": staff,
        "students": students,
        "query": query
    })
    
from datetime import date
from django.db import transaction
from django.utils import timezone


@login_required
def staff_attendance(request):
    staff = get_staff_profile(request.user)

    students = get_assigned_students(staff).filter(
        is_active=True
    )

    today = timezone.localdate()

    if request.method == "POST":
        attendance_date = request.POST.get("date") or str(today)

        try:
            attendance_date = date.fromisoformat(attendance_date)
        except ValueError:
            messages.error(request, "Invalid attendance date.")
            return redirect("staff:attendance")

        with transaction.atomic():
            for student in students:
                status = request.POST.get(
                    f"status_{student.pk}"
                )

                if status not in ["PRESENT", "ABSENT", "LATE"]:
                    continue

                reason = request.POST.get(
                    f"reason_{student.pk}", ""
                )

                Attendance.objects.update_or_create(
                    student=student,
                    date=attendance_date,
                    defaults={
                        "status": status,
                        "method": "MANUAL",
                        "marked_by": staff,
                        "manual_reason": reason,
                    }
                )

        messages.success(
            request, "Attendance saved successfully!"
        )
        return redirect("staff:attendance")

    records = Attendance.objects.filter(
        student__in=students,
        date=today
    )

    attendance_map = {
        record.student_id: record
        for record in records
    }

    return render(request, "staff/attendance.html", {
        "staff": staff,
        "students": students,
        "attendance_map": attendance_map,
        "today": today,
    })


@login_required
def staff_qr_attendance(request):
    staff = get_staff_profile(request.user)

    # QR verification must be completed by a secure,
    # server-side location and token validation flow.
    return render(request, "staff/qr_attendance.html", {
        "staff": staff,
        "message": "QR attendance verification"
    })


@login_required
def staff_attendance_history(request):
    staff = get_staff_profile(request.user)

    records = Attendance.objects.filter(
        student__department=staff.department,
        student__section=staff.section
    ).select_related(
        "student", "marked_by"
    ).order_by("-date")

    selected_date = request.GET.get("date")

    if selected_date:
        try:
            selected_date = date.fromisoformat(selected_date)
            records = records.filter(date=selected_date)
        except ValueError:
            messages.error(request, "Invalid date.")

    return render(request, "staff/attendance_history.html", {
        "staff": staff,
        "records": records,
    })
                
        
