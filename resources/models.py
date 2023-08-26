from django.db import models

class SharePost(models.Model):
    viewNum = models.PositiveIntegerField("조회수", default=0)
    title = models.CharField("포스트 제목", max_length=100)
    content = models.TextField("포스트 내용")
    createdDate = models.DateTimeField("생성일시", auto_now_add=True)
    thumbnailImage = models.ImageField(
        "썸네일",
        upload_to="resources/share",
        blank=True,
    )

    def __str__(self):
        return self.title