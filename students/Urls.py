from django.urls import path
from . import views

urlpatterns = [
    path(
        'dashboard/',
        views.student_dashboard,
        name='student_dashboard'
        'complaint/'
        views.student_complaint'
    ),
]
