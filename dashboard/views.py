from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render

from .models import (
    Department,
    Student,
    StaffMember,
    Attendance,
    Complaint
)

from .forms import (
    DepartmentForm,
    StudentForm,
    StaffForm,
    AttendanceForm,
    ComplaintForm
)


def is_admin(user):
    return user.is_authenticated and (
        user.is_superuser or user.is_staff
    )


admin_only = user_passes_test(
    is_admin,
    login_url="login"
)


@login_required
@admin_only
def home(request):

    depts = list(
        Department.objects.annotate(
            student_total=Count("students")
        )
    )

    total_att = Attendance.objects.count()

    present = Attendance.objects.filter(
        status="Present"
    ).count()

    rate = round(
        present * 100 / total_att, 1
    ) if total_att else 0

    context = {
        "departments": depts,

        "students": Student.objects.select_related(
            "department"
        ),

        "staff_members": StaffMember.objects.select_related(
            "department"
        ),

        "attendance_records": Attendance.objects.select_related(
            "student"
        )[:100],

        "complaints": Complaint.objects.all(),

        "total_students": Student.objects.count(),

        "total_staff": StaffMember.objects.count(),

        "attendance_rate": rate,

        "not_present_rate": round(100 - rate, 1),

        "open_complaints": Complaint.objects.exclude(
            status="Resolved"
        ).count(),

        "department_labels": [
            d.name for d in depts
        ],

        "department_values": [
            d.student_total for d in depts
        ],

        "staff_department_values": [
            d.staff_members.count() for d in depts
        ],

        "complaint_labels": [
            "Open",
            "In Progress",
            "Resolved"
        ],

        "complaint_values": [
            Complaint.objects.filter(status="Open").count(),
            Complaint.objects.filter(status="In Progress").count(),
            Complaint.objects.filter(status="Resolved").count()
        ]
    }

    return render(
        request,
        "dashboard/dashboard.html",
        context
    )


CONFIG = {
    "department": (
        Department,
        DepartmentForm,
        "Department"
    ),

    "student": (
        Student,
        StudentForm,
        "Student"
    ),

    "staff": (
        StaffMember,
        StaffForm,
        "Staff"
    ),

    "attendance": (
        Attendance,
        AttendanceForm,
        "Attendance"
    ),

    "complaint": (
        Complaint,
        ComplaintForm,
        "Complaint"
    )
}


@login_required
@admin_only
def add(request, kind):

    if kind not in CONFIG:
        return redirect("dashboard_home")

    _, form_cls, label = CONFIG[kind]

    form = form_cls(request.POST or None)

    if request.method == "POST" and form.is_valid():

        form.save()

        messages.success(
            request,
            f"{label} added successfully."
        )

        return redirect("dashboard_home")

    return render(
        request,
        "dashboard/form.html",
        {
            "form": form,
            "heading": f"Add {label}"
        }
    )


@login_required
@admin_only
def edit(request, kind, pk):

    if kind not in CONFIG:
        return redirect("dashboard_home")

    model, form_cls, label = CONFIG[kind]

    obj = get_object_or_404(model, pk=pk)

    form = form_cls(
        request.POST or None,
        instance=obj
    )

    if request.method == "POST" and form.is_valid():

        form.save()

        messages.success(
            request,
            f"{label} updated successfully."
        )

        return redirect("dashboard_home")

    return render(
        request,
        "dashboard/form.html",
        {
            "form": form,
            "heading": f"Edit {label}"
        }
    )


@login_required
@admin_only
def delete(request, kind, pk):

    if kind not in CONFIG:
        return redirect("dashboard_home")

    obj = get_object_or_404(
        CONFIG[kind][0],
        pk=pk
    )

    if request.method == "POST":

        obj.delete()

        messages.success(
            request,
            "Record deleted successfully."
        )

        return redirect("dashboard_home")

    return render(
        request,
        "dashboard/confirm_delete.html",
        {
            "object": obj
        }
    )
