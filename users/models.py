from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    profile_image = models.ImageField(
        "프로필 이미지", upload_to="users/profile", blank=True,
        default='default_profile_image.png',
        null = True,
    )

    short_description = models.TextField("소개글", blank=True)

    nickname = models.CharField("닉네임", max_length=8, unique=True, error_messages = {'unique': '이미 존재하는 이름 또는 닉네임입니다.'},
                                help_text='닉네임은 최대 8글자 입니다.',
    )

    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)