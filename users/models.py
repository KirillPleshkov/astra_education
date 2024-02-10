from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUserManager(BaseUserManager):
    """Менеджер пользователя реализующий создание пользователя по email"""

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


def get_student_role():
    return Role.objects.get(name='Студент').id


class CustomUser(AbstractUser):
    """Модель пользователя"""
    username = None
    email = models.EmailField(unique=True, max_length=100)
    first_name = models.CharField(max_length=100, verbose_name='имя')
    last_name = models.CharField(max_length=100, verbose_name='фамилия')

    role = models.ForeignKey('Role', on_delete=models.PROTECT, verbose_name='роль', default=get_student_role)
    curriculum = models.ForeignKey('curriculum.Curriculum', on_delete=models.PROTECT, verbose_name='учебный план',
                                   null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='название')

    class Meta:
        verbose_name = 'роль'
        verbose_name_plural = 'роли'

    def __str__(self):
        return self.name
