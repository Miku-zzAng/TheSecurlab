from django.contrib import admin
from community.models import Post, PostImage, Comment
import admin_thumbnails # 라이브러리 import

# 각 모델에 대한 CRUD(Create, Read, Update, Delete) 연산을 더 편리하게 수행
# 인라인: 한 모델과 다른 모델 연결.

# '인라인 형태'로 관리자 페이지에서 보여줄 설정 정의
class CommentInline(admin.TabularInline):
    model = Comment # 이 클래스는 Comment 모델을 대상한다.
    extra = 1 # 밑에 새로운 생성폼 한개만 추가.

# PostImage 인라인 설정
@admin_thumbnails.thumbnail("photo") #photo 필드의 이미지를 썸네일로 보여줄수 있음.
class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 1



@admin.register(Post) # Post 모델을 관리자 페이지에 등록
class PostAdmin(admin.ModelAdmin):
    list_display = [
        "title","id","writer","createdDate",
    ]
    inlines = [ # Post 객체 수정하거나 보여줄때 함께 보여줄 인라인 객체들 지정
        PostImageInline, # 필드셋 밑에 이미지,댓글 편집 가능하게됨
        CommentInline,
    ]
    fieldsets = [ # 편집 뷰에서 어떤 편집대상들을 그룹핑 할것인지.
        ("기본 정보", {"fields": ("title", "content", "writer")}),
    ]

@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    list_display = [
        "targetPost", "photo"
    ]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = [
        "content","id","targetPost","writer","createdDate"
    ]