from django.urls import path
from . import views

urlpatterns = [
    path(
        'dashboard/',
        views.student_dashboard,
        name='student_dashboard'
        'complaint/',
        views.student_complaint'
        name='students_complwints'
            
        'correction/',
            views.attandance_correction'
            name='attandance_correction'
                'request-history/'
                views.student_requests,
                name='student_request,
        
    ),
]
