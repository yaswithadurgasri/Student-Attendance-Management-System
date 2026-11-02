
from django.urls import path
from . import views

app_name = "staff"

urlpatterns = [
    path(
        "dashboard/",
        views.staff_dashboard,
        name="dashboard"
    ),

    path(
        "attendance/history/",
        views.staff_attendance_history,
        name="attendance_history"
    ),

    path(
        "performance/",
        views.staff_performance,
        name="performance"
    ),

    path(
        "timetable/",
        views.staff_timetable,
        name="timetable"
    ),

    path(
        "complaints/",
        views.staff_complaints,
        name="complaints"
    ),

    path(
        "complaints/history/",
        views.staff_complaint_history,
        name="complaint_history"
    ),

    path(
        "reports/",
        views.staff_reports,
        name="reports"
    ),

    path(
        "settings/",
        views.staff_settings,
        name="settings"
    ),
    
path("students/add/", views.staff_student_add, name="student_add"),

path(
    "students/edit/<int:student_id>/",
    views.staff_student_edit,
    name="student_edit"
),

path(
    "students/delete/<int:student_id>/",
    views.staff_student_delete,
    name="student_delete"
),

path(
    "students/search/",
    views.staff_student_search,
    name="student_search"
),
    
path(
    "attendance/",
    views.staff_attendance,
    name="attendance"
),

path(
    "attendance/qr/",
    views.staff_qr_attendance,
    name="qr_attendance"
),
    
path(
    "performance/",
    views.staff_performance,
    name="performance"
),

path(
    "performance/add/<int:student_id>/",
    views.staff_add_performance,
    name="add_performance"
),

path(
    "performance/edit/<int:record_id>/",
    views.staff_edit_performance,
    name="edit_performance"
),
    
path(
    "complaints/",
    views.staff_complaints,
    name="complaints"
),

path(
    "complaints/update/<int:complaint_id>/",
    views.staff_update_complaint,
    name="update_complaint"
),

path(
    "complaints/submit/",
    views.staff_submit_complaint,
    name="submit_complaint"
),
    

    
    
]
