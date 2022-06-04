from django.db import models, transaction
from django.utils import timezone
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)


class UserManager(BaseUserManager):
    """
    the User Manager class is responsible for creating a user and a superuser
    """
    def _create_user(self, email, username, password, **extra_fields):
        if not username:
            raise ValueError("Username and password must be set")
        if not password:
            raise ValueError("Username and password must be set")
        try:
            with transaction.atomic():
                user = self.model(email=email, username=username, **extra_fields)
                user.set_password(password)
                user.save(using=self.db)
                return user
        except:
            raise

    def create_user(self, email, username, password, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, username, password, **extra_fields)

    def create_superuser(self, email, username, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(email, username, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.
    {
        "post_article":{
            "favorite":False,
            "rate":0,
        }
    }

    """

    # main_auth
    password = models.CharField("Пароль", max_length=100)
    email = models.EmailField("Мыло", max_length=100, unique=True)
    username = models.CharField("Имя пользователя", max_length=100, unique=True)
    is_active = models.BooleanField(default=True)

    # user_data
    date_joined = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)

    # posts
    posts_info = models.TextField(default="{}")

    # for_api
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "password"]
    objects = UserManager()

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        return self

    def __str__(self):
        return self.username
