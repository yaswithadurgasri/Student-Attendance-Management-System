
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Information", {"fields": ("role",)}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional Information", {"fields": ("role",)}),
    )

admin.site.register(User, CustomUserAdmin)
