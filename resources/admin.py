from django.contrib import admin
from resources.models import SharePost
from django.utils.html import format_html
from django.db import models
from django import forms

@admin.register(SharePost)
class SharePostAdmin(admin.ModelAdmin):
    list_display = [
        "title", "id", "thumbnail_preview", "group_id",
    ]
    fieldsets = [
        ("기본 정보", {"fields": ("title", "content", "subinfo", "thumbnailImage", "group_id")}),
    ]

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == "title":
            kwargs['widget'] = forms.TextInput(attrs={'size': '80'})  # 여기에서 50은 원하는 크기로 조절할 수 있습니다.
        if db_field.name == "subinfo":
            kwargs['widget'] = forms.TextInput(attrs={'size': '80'})  # 여기에서 80은 원하는 크기로 조절할 수 있습니다.
        return super().formfield_for_dbfield(db_field, **kwargs)

    def thumbnail_preview(self, obj):
        return format_html('<img src="{}" width="50" height="50" />', obj.thumbnailImage.url)

    def __str__(self):
        return self.title