from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, BaseUserManager, PermissionsMixin

# 먼저 CustomUserManager 클래스를 정의합니다.
class CustomUserManager(BaseUserManager):
    def _create_user(self, username, email=None, password=None, **extra_fields):
        # 아래의 코드는 기본 _create_user의 로직에 근거한 것입니다. 필요에 따라 조정할 수 있습니다.
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if 'nickname' not in extra_fields:
            extra_fields['nickname'] = username

        return self._create_user(username, email, password, **extra_fields)


# 그리고 나서 User 클래스를 정의합니다.
class User(AbstractUser):
    profile_image = models.ImageField(
        "프로필 이미지", upload_to="users/profile", blank=True,
        default='default_profile_image.png',
        null=True,
    )
    short_description = models.TextField("소개글", blank=True)
    nickname = models.CharField(
        "닉네임", max_length=8, unique=True,
        error_messages={'unique': '이미 존재하는 이름 또는 닉네임입니다.'},
        help_text='닉네임은 최대 8글자 입니다.',
    )
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    objects = CustomUserManager()
