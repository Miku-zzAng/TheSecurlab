from django.contrib import admin
from community.models import Post, PostImage, Comment
import admin_thumbnails


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1


@admin_thumbnails.thumbnail("photo")
class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 1


@admin_thumbnails.thumbnail("thumbnailImage")
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        "title","id","writer","createdDate",
    ]
    inlines = [
        PostImageInline,
        CommentInline,
    ]
    fieldsets = [
        ("기본 정보", {"fields": ("title", "content", "writer")}),
    ]


@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    list_display = [
        "targetPost", "photo"
    ]


@admin.register(Comment)
class PostImageAdmin(admin.ModelAdmin):
    list_display = [
        "id","targetPost", "content", "writer","createdDate"
    ]