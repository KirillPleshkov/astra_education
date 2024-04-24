from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

from astra_education import settings


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


class CustomUser(AbstractUser):
    """Модель пользователя"""
    username = None
    email = models.EmailField(unique=True, max_length=100)
    first_name = models.CharField(max_length=100, verbose_name='имя')
    last_name = models.CharField(max_length=100, verbose_name='фамилия')

    class Roles(models.TextChoices):
        STUDENT = "S", "Студент"
        TEACHER = "T", "Преподаватель"

    role = models.CharField(
        max_length=1,
        choices=Roles.choices,
        default=Roles.STUDENT,
        verbose_name='роль'
    )
    linguist_roles = models.ManyToManyField('LinguistsRoles', blank=True, verbose_name='Лингвистическая роль')
    curriculum = models.ForeignKey('curriculum.Curriculum', on_delete=models.PROTECT, verbose_name='учебный план',
                                   null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def clean_linguist_roles(self):
        from django.core.exceptions import ValidationError
        if self.role == get_user_model().Roles.STUDENT and self.linguist_roles.count():
            raise ValidationError('Пользователь с ролью студент не может иметь лингвистическую роль')


class LinguistsRoles(models.Model):
    class LinguistsRolesChose(models.TextChoices):
        MODULE_CHANGE = "M", "Лингвист модулей"
        DISCIPLINE_CHANGE = "D", "Лингвист дисциплин"
        CURRICULUM_CHANGE = "C", "Лингвист учебных планов"

    linguist_role = models.CharField(
        max_length=1,
        choices=LinguistsRolesChose.choices,
        verbose_name='роль',
        unique=True
    )

    class Meta:
        verbose_name = 'роль лингвиста'
        verbose_name_plural = 'роли лингвиста'

    def __str__(self):
        return self.LinguistsRolesChose(self.linguist_role).label
