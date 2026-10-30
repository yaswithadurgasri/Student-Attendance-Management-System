
from django.urls import path
from . import views

app_name = "attendance"

urlpatterns = [

    # Teacher URLs
    path("", views.attendance_page, name="attendance_page"),
    path("start/", views.start_attendance, name="start_attendance"),
    path("login/", views.teacher_login, name="teacher_login"),

    # Student URLs
    path("student-login/", views.student_login, name="student_login"),
    path("student-dashboard/", views.student_dashboard, name="student_dashboard"),

    # QR Attendance URLs
    path("active-attendance/", views.active_attendance, name="active_attendance"),
    path("get-active-qr/", views.get_active_qr, name="get_active_qr"),
    path("mark-qr/", views.mark_qr_attendance, name="mark_qr_attendance"),

    # Report URLs
    path("teacher-attendance/", views.teacher_attendance, name="teacher_attendance"),
    path("date-wise-report/", views.date_wise_report, name="date_wise_report"),
    path("subject-wise-report/", views.subject_wise_report, name="subject_wise_report"),

]
