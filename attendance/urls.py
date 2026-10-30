from django.urls import path
from . import views

urlpatterns = [
    path('teacher-attendance/', views.teacher_attendance, name='teacher_attendance'),
    path('date-wise-report/', views.date_wise_report, name='date_wise_report'),
    path('subject-wise-report/', views.subject_wise_report, name='subject_wise_report'),
]