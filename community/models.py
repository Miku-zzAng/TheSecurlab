from django.db import models


class Post(models.Model):
    title = models.CharField("게시물 제목", max_length=100)
    content = models.TextField("포스트 내용")
    createdDate = models.DateTimeField("생성일시", auto_now_add=True)
    writer = models.ForeignKey(
        "users.User", verbose_name="작성자", on_delete=models.CASCADE
    )
    modify_date = models.DateTimeField("수정일시", null=True, blank=True)
    thumbnailImage = models.ImageField(
        "썸네일",
        upload_to="community/board",
        blank=True,
    )

    def __str__(self):
        return self.title


class PostImage(models.Model):
    targetPost = models.ForeignKey(Post, verbose_name="게시물", on_delete=models.CASCADE)
    photo = models.ImageField(
        "사진",
        upload_to="community/board",
        blank=True,
    )


class Comment(models.Model):
    targetPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField("댓글 내용")
    createdDate = models.DateTimeField("생성일시", auto_now_add=True)
    modify_date = models.DateTimeField("수정일시", null=True, blank=True)
    writer = models.ForeignKey(
        "users.User", verbose_name="작성자", on_delete=models.CASCADE
    )

    def __sts__(self):
        return f"{self.targetPost.title}의 댓글 (ID:{self.id})"
