from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.name} ({self.code})"


class Student(models.Model):
    student_id = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=120)
    email = models.EmailField(blank=True)

    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="students"
    )

    year = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return f"{self.name} ({self.student_id})"


class StaffMember(models.Model):
    staff_id = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=120)
    email = models.EmailField(blank=True)

    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="staff_members"
    )

    def __str__(self):
        return f"{self.name} ({self.staff_id})"


class Attendance(models.Model):

    STATUS_CHOICES = [
        ("Present", "Present"),
        ("Absent", "Absent"),
        ("Late", "Late"),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="attendance_records"
    )

    date = models.DateField()

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="Present"
    )

    class Meta:
        ordering = ["-date", "student__name"]

        constraints = [
            models.UniqueConstraint(
                fields=["student", "date"],
                name="unique_student_attendance_per_day"
            )
        ]

    def __str__(self):
        return f"{self.student} - {self.date} - {self.status}"


class Complaint(models.Model):

    SOURCE_CHOICES = [
        ("Student", "Student"),
        ("Staff", "Staff"),
    ]

    STATUS_CHOICES = [
        ("Open", "Open"),
        ("In Progress", "In Progress"),
        ("Resolved", "Resolved"),
    ]

    source = models.CharField(
        max_length=10,
        choices=SOURCE_CHOICES
    )

    person_name = models.CharField(max_length=120)
    subject = models.CharField(max_length=160)
    description = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Open"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.subject
