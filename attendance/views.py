
import io
import base64
import secrets
import qrcode

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_GET, require_POST

from students.models import Student
from teachers.models import Teacher
from .models import (
    Subject,
    Attendance,
    AttendanceSession,
    AttendanceRecord,
)


# ==========================================
# MANUAL ATTENDANCE - FRIENDS' MODULE
# ==========================================

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


# ==========================================
# DATE-WISE REPORT
# ==========================================

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


# ==========================================
# SUBJECT-WISE REPORT
# ==========================================

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


# ==========================================
# QR ATTENDANCE - TEACHER MODULE
# ==========================================

@require_POST
def start_attendance(request):

    if not request.user.is_authenticated:
        return JsonResponse({"error": "Please log in first."}, status=401)

    if request.user.role != "TEACHER":
        return JsonResponse(
            {"error": "Only teachers can start attendance."},
            status=403
        )

    subject = request.POST.get("subject", "").strip()

    if not subject:
        return JsonResponse(
            {"error": "Please enter a subject."},
            status=400
        )

    session = AttendanceSession.objects.create(
        teacher=request.user,
        subject=subject,
        session_token=secrets.token_urlsafe(32),
        is_active=True,
    )

    qr_content = (
        f"attendance-session:{session.id}:"
        f"{session.session_token}"
    )

    qr_image = qrcode.make(qr_content)

    buffer = io.BytesIO()
    qr_image.save(buffer, format="PNG")

    qr_base64 = base64.b64encode(
        buffer.getvalue()
    ).decode("utf-8")

    return JsonResponse({
        "session_id": session.id,
        "subject": session.subject,
        "qr_code": f"data:image/png;base64,{qr_base64}",
        "message": "Attendance session started."
    })


@login_required
def attendance_page(request):

    if request.user.role != "TEACHER":
        return HttpResponseForbidden("Teacher access only.")

    return render(request, "attendance/start_attendance.html")


# ==========================================
# TEACHER LOGIN
# ==========================================

def teacher_login(request):
    error = ""

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None and user.role == "TEACHER":
            login(request, user)
            return redirect("attendance:attendance_page")

        error = "Invalid teacher username or password."

    return render(
        request,
        "attendance/teacher_login.html",
        {"error": error}
    )


# ==========================================
# STUDENT LOGIN
# ==========================================

def student_login(request):
    error = ""

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is None:
            error = "Username or password is incorrect."

        elif user.role != "STUDENT":
            error = "This account is not a student account."

        elif not user.is_active:
            error = "This account is inactive."

        else:
            login(request, user)
            return redirect("attendance:student_dashboard")

    return render(
        request,
        "attendance/student_login.html",
        {"error": error}
    )


# ==========================================
# STUDENT DASHBOARD
# ==========================================

@login_required
def student_dashboard(request):

    if request.user.role != "STUDENT":
        return HttpResponseForbidden("Student access only.")

    return render(
        request,
        "attendance/student_dashboard.html"
    )


# ==========================================
# CHECK ACTIVE ATTENDANCE
# ==========================================

@login_required
@require_GET
def active_attendance(request):

    if request.user.role != "STUDENT":
        return JsonResponse({"error": "Students only."}, status=403)

    session = AttendanceSession.objects.filter(
        is_active=True
    ).select_related("teacher").order_by("-start_time").first()

    if not session:
        return JsonResponse({"active": False})

    already_marked = AttendanceRecord.objects.filter(
        session=session,
        student=request.user
    ).exists()

    return JsonResponse({
        "active": True,
        "session_id": session.id,
        "subject": session.subject,
        "teacher": session.teacher.username,
        "already_marked": already_marked
    })


# ==========================================
# GET QR NOTIFICATION
# ==========================================

@login_required
@require_GET
def get_active_qr(request):

    if request.user.role != "STUDENT":
        return JsonResponse(
            {"error": "Students only."},
            status=403
        )

    session = AttendanceSession.objects.filter(
        is_active=True
    ).order_by("-start_time").first()

    if not session:
        return JsonResponse(
            {"error": "No active attendance session."},
            status=404
        )

    qr_content = (
        f"attendance-session:{session.id}:"
        f"{session.session_token}"
    )

    qr_image = qrcode.make(qr_content)

    buffer = io.BytesIO()
    qr_image.save(buffer, format="PNG")

    qr_base64 = base64.b64encode(
        buffer.getvalue()
    ).decode("utf-8")

    return JsonResponse({
        "qr_code": f"data:image/png;base64,{qr_base64}",
        "qr_data": qr_content,
        "subject": session.subject,
        "session_id": session.id
    })


# ==========================================
# MARK QR ATTENDANCE
# ==========================================

@login_required
@require_POST
def mark_qr_attendance(request):

    if request.user.role != "STUDENT":
        return JsonResponse(
            {"error": "Students only."},
            status=403
        )

    qr_data = request.POST.get("qr_data", "")

    try:
        prefix, session_id, token = qr_data.split(":", 2)

        if prefix != "attendance-session":
            raise ValueError("Invalid QR")

        session = AttendanceSession.objects.get(
            id=int(session_id),
            is_active=True
        )

    except (ValueError, AttendanceSession.DoesNotExist):
        return JsonResponse({
            "success": False,
            "message": "Invalid or expired QR code."
        }, status=400)

    if not secrets.compare_digest(session.session_token, token):
        return JsonResponse({
            "success": False,
            "message": "Invalid QR security token."
        }, status=400)

    record, created = AttendanceRecord.objects.get_or_create(
        session=session,
        student=request.user
    )

    return JsonResponse({
        "success": True,
        "message": (
            "Attendance marked successfully!"
            if created else
            "Attendance already marked."
        )
    })
