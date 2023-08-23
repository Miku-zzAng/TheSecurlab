from django.contrib import admin
from community.models import Post, PostImage, Comment


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
        "id","title","content","writer","createdDate","thumbnailImage"
    ]
    inlines = [
        PostImageInline,
        CommentInline,
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