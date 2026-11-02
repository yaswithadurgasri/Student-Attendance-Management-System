
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
]
