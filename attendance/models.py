
from django.db import models
from students.models import Student
from teachers.models import Teacher


class Subject(models.Model):
    subject_code = models.CharField(max_length=20, unique=True)
    subject_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.subject_code} - {self.subject_name}"


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('PRESENT', 'Present'),
        ('ABSENT', 'Absent'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'subject', 'date'],
                name='unique_student_subject_date'
            )
        ]

    def __str__(self):
        return f"{self.student} - {self.subject} - {self.date} - {self.status}"
from django.conf import settings


class AttendanceSession(models.Model):
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="attendance_sessions"
    )
    subject = models.CharField(max_length=100)
    session_token = models.CharField(max_length=100, unique=True)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.subject} - {self.teacher.username}"


class AttendanceRecord(models.Model):
    session = models.ForeignKey(
        AttendanceSession,
        on_delete=models.CASCADE,
        related_name="records"
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="attendance_records"
    )
    marked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["session", "student"],
                name="unique_student_per_attendance_session"
            )
        ]

    def __str__(self):
        return f"{self.student.username} - {self.session.subject}"
