from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = [
        ("기본 정보", {"fields": ("username", "nickname", "password", "email")}),
        ("추가 필드", {"fields": ("profile_image", "short_description")}),
        ("권한 여부",  {"fields": ("is_active", "is_staff", "is_superuser",)}),
        ("Date", {"fields": ("last_login", "date_joined")}),
    ]