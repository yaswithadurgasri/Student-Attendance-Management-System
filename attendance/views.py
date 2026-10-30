from django.shortcuts import render, redirect
from django.contrib import messages
from students.models import Student
from teachers.models import Teacher
from attendance.models import Subject, Attendance


def teacher_attendance(request):
    students = Student.objects.all()
    subjects = Subject.objects.all()

    if request.method == 'POST':
        date = request.POST.get('date')
        subject_id = request.POST.get('subject')

        teacher = Teacher.objects.first()

        if not teacher:
            messages.error(request, 'No teacher available in database.')
            return redirect('teacher_attendance')

        if not date or not subject_id:
            messages.error(request, 'Please select date and subject.')
            return redirect('teacher_attendance')

        try:
            subject = Subject.objects.get(id=subject_id)
        except Subject.DoesNotExist:
            messages.error(request, 'Invalid subject selected.')
            return redirect('teacher_attendance')

        for student in students:
            status = request.POST.get(f'status_{student.id}')

            if status in ['PRESENT', 'ABSENT']:
                Attendance.objects.update_or_create(
                    student=student,
                    subject=subject,
                    date=date,
                    defaults={
                        'teacher': teacher,
                        'status': status,
                    }
                )

        messages.success(request, 'Attendance saved successfully!')
        return redirect('teacher_attendance')

    return render(
        request,
        'attendance/teacher_attendance.html',
        {
            'students': students,
            'subjects': subjects,
        }
    )
def date_wise_report(request):
    date = request.GET.get('date')
    records = Attendance.objects.none()

    if date:
        records = Attendance.objects.filter(date=date).select_related(
            'student', 'teacher', 'subject'
        )

    return render(
        request,
        'attendance/date_wise_report.html',
        {'records': records, 'selected_date': date}
    )


def subject_wise_report(request):
    subject_id = request.GET.get('subject')
    subjects = Subject.objects.all()
    records = Attendance.objects.none()

    if subject_id:
        records = Attendance.objects.filter(
            subject_id=subject_id
        ).select_related('student', 'teacher', 'subject')

    return render(
        request,
        'attendance/subject_wise_report.html',
        {
            'records': records,
            'subjects': subjects,
            'selected_subject': subject_id,
        }
    )