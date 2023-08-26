from django.contrib import admin
from resources.models import SharePost
from django.utils.html import format_html


@admin.register(SharePost)
class SharePostAdmin(admin.ModelAdmin):
    list_display = [
        "title", "id", "content", "thumbnail_preview",
    ]
    fieldsets = [ 
        ("기본 정보", {"fields": ("title", "content", "subinfo", "thumbnailImage",)}),
    ]

    def thumbnail_preview(self, obj):
        return format_html('<img src="{}" width="50" height="50" />', obj.thumbnailImage.url)

    def __str__(self):
        return self.title