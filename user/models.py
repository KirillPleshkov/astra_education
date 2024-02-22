from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

from astra_education import settings


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='название')

    class Meta:
        verbose_name = 'роль'
        verbose_name_plural = 'роли'

    def __str__(self):
        return self.name


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
    return Role.objects.get(name=settings.STUDENT_NAME).id


class CustomUser(AbstractUser):
    """Модель пользователя"""
    username = None
    email = models.EmailField(unique=True, max_length=100)
    first_name = models.CharField(max_length=100, verbose_name='имя')
    last_name = models.CharField(max_length=100, verbose_name='фамилия')

    role = models.ForeignKey('Role', on_delete=models.PROTECT, verbose_name='роль', default=get_student_role)
    linguist_roles = models.ManyToManyField('LinguistRole', through='LinguistRoleUser', related_name='users')
    curriculum = models.ForeignKey('curriculum.Curriculum', on_delete=models.PROTECT, verbose_name='учебный план',
                                   null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.email


class LinguistRole(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='название')

    class Meta:
        verbose_name = 'роль лингвиста'
        verbose_name_plural = 'роли лингвиста'

    def __str__(self):
        return self.name


class LinguistRoleUser(models.Model):
    """Связь многие ко многим ролей лингвистов и пользователей"""

    linguist_role = models.ForeignKey(LinguistRole, on_delete=models.CASCADE, verbose_name='роль лингвиста')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='пользователь')

    class Meta:
        verbose_name = 'роль лингвиста'
        verbose_name_plural = 'роли лингвиста'
        unique_together = ('linguist_role', 'user')

    def __str__(self):
        return f'Роль лингвиста: {self.linguist_role.name}, пользователь: {self.user}'
