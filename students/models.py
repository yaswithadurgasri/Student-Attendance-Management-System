from django.db import models


class Student(models.Model):
    student_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    section = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.student_id} - {self.name}"
