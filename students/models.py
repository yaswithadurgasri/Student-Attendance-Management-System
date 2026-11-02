from django.db import models


class Student(models.Model):
    student_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    section = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.student_id} - {self.name}"
        class StudentComplaint(models.Model):

    COMPLAINT_TYPES = [
        ('staff', 'Staff'),
        ('admin', 'Admin'),
    ]

    STATUS_CHOICES = [
        ('Submitted', 'Submitted'),
        ('Under Review', 'Under Review'),
        ('Resolved', 'Resolved'),
    ]

    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE
    )

    complaint_to = models.CharField(
        max_length=10,
        choices=COMPLAINT_TYPES
    )

    subject = models.CharField(max_length=150)

    description = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Submitted'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject
class AttendanceCorrection(models.Model):

    STATUS_CHOICES = [
        ('Submitted', 'Submitted'),
        ('Under Review', 'Under Review'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE
    )

    attendance_date = models.DateField()

    subject = models.CharField(max_length=100)

    reason = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Submitted'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.name} - {self.attendance_date}"
