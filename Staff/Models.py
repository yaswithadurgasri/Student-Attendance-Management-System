
from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# -------------------------
# 1. DEPARTMENT
# -------------------------

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# -------------------------
# 2. SECTION
# -------------------------

class Section(models.Model):
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="sections"
    )
    name = models.CharField(max_length=50)
    academic_year = models.CharField(max_length=20)

    class Meta:
        unique_together = ("department", "name", "academic_year")

    def __str__(self):
        return f"{self.name} - {self.department.name}"


# -------------------------
# 3. SUBJECT
# -------------------------

class Subject(models.Model):
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)
    subject_code = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.name


# -------------------------
# 4. STAFF PROFILE
# -------------------------

class StaffProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="staff_profile"
    )

    staff_id = models.CharField(max_length=30, unique=True)
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    section = models.ForeignKey(
        Section,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    subjects = models.ManyToManyField(Subject, blank=True)

    designation = models.CharField(max_length=100, blank=True)
    academic_year = models.CharField(max_length=20, blank=True)
    phone = models.CharField(max_length=15, blank=True)

    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.staff_id} - {self.user}"


# -------------------------
# 5. STUDENT
# -------------------------

class Student(models.Model):
    student_id = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=150)

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE
    )
    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE
    )

    academic_year = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=15, blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_id} - {self.name}"


# -------------------------
# 6. ATTENDANCE
# -------------------------

class Attendance(models.Model):

    STATUS_CHOICES = [
        ("PRESENT", "Present"),
        ("ABSENT", "Absent"),
        ("LATE", "Late"),
    ]

    METHOD_CHOICES = [
        ("QR", "QR Attendance"),
        ("MANUAL", "Manual Attendance"),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="attendance_records"
    )

    date = models.DateField()
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES
    )

    method = models.CharField(
        max_length=10,
        choices=METHOD_CHOICES,
        default="MANUAL"
    )

    marked_by = models.ForeignKey(
        StaffProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    manual_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("student", "date")
        ordering = ["-date"]

    def __str__(self):
        return f"{self.student.student_id} - {self.date} - {self.status}"


# -------------------------
# 7. PERFORMANCE & REMARKS
# -------------------------

class PerformanceRemark(models.Model):

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="performance_records"
    )

    staff = models.ForeignKey(
        StaffProfile,
        on_delete=models.CASCADE
    )

    subject = models.ForeignKey(
        Subject,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    academic_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )

    participation = models.TextField(blank=True)
    assignment_performance = models.TextField(blank=True)
    behaviour_remarks = models.TextField(blank=True)
    improvement_suggestions = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Performance - {self.student.name}"


# -------------------------
# 8. COMPLAINTS
# -------------------------

class Complaint(models.Model):

    ROLE_CHOICES = [
        ("STUDENT", "Student"),
        ("STAFF", "Staff"),
    ]

    RECIPIENT_CHOICES = [
        ("TEACHER", "Teacher"),
        ("ADMIN", "Admin"),
    ]

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("IN_PROGRESS", "In Progress"),
        ("RESOLVED", "Resolved"),
        ("FORWARDED", "Forwarded to Admin"),
    ]

    submitted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="submitted_complaints"
    )

    student = models.ForeignKey(
        Student,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    target_teacher = models.ForeignKey(
        StaffProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    source_role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES
    )

    recipient = models.CharField(
        max_length=10,
        choices=RECIPIENT_CHOICES
    )

    category = models.CharField(max_length=100)
    subject = models.CharField(max_length=200)
    description = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING"
    )

    resolution_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject


# -------------------------
# 9. TIMETABLE
# -------------------------

class TimetableEntry(models.Model):

    DAYS = [
        ("MON", "Monday"),
        ("TUE", "Tuesday"),
        ("WED", "Wednesday"),
        ("THU", "Thursday"),
        ("FRI", "Friday"),
        ("SAT", "Saturday"),
    ]

    staff = models.ForeignKey(
        StaffProfile,
        on_delete=models.CASCADE
    )

    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE
    )

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE
    )

    day = models.CharField(max_length=3, choices=DAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.subject.name} - {self.day}"
              
