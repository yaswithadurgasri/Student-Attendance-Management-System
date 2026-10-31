from django import forms

from .models import (
    Department,
    Student,
    StaffMember,
    Attendance,
    Complaint
)


class BaseStyledForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs["class"] = "form-select"
            else:
                field.widget.attrs["class"] = "form-control"


class DepartmentForm(BaseStyledForm):

    class Meta:
        model = Department
        fields = ["name", "code"]


class StudentForm(BaseStyledForm):

    class Meta:
        model = Student
        fields = [
            "student_id",
            "name",
            "email",
            "department",
            "year"
        ]


class StaffForm(BaseStyledForm):

    class Meta:
        model = StaffMember
        fields = [
            "staff_id",
            "name",
            "email",
            "department"
        ]


class AttendanceForm(BaseStyledForm):

    date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"})
    )

    class Meta:
        model = Attendance
        fields = [
            "student",
            "date",
            "status"
        ]


class ComplaintForm(BaseStyledForm):

    class Meta:
        model = Complaint

        fields = [
            "source",
            "person_name",
            "subject",
            "description",
            "status"
        ]

        widgets = {
            "description": forms.Textarea(attrs={"rows": 4})
              }
