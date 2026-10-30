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