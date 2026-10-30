from django.db import models


class Teacher(models.Model):
    teacher_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.teacher_id} - {self.name}"
