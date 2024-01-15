from django.contrib.auth import get_user_model
from django.db import models

user_model = get_user_model()


class Discipline(models.Model):
    """Дисциплина"""

    name = models.CharField(max_length=50, verbose_name='название')
    short_description = models.TextField(blank=True, default='', max_length=500, verbose_name='краткое описание')

    teachers = models.ManyToManyField(user_model, through='DisciplineUser')

    class Meta:
        verbose_name = 'дисциплина'
        verbose_name_plural = 'дисциплины'

    def __str__(self):
        return self.name


class Section(models.Model):
    """Раздел дисциплины"""

    name = models.CharField(max_length=50, verbose_name='название', unique=True)

    class Meta:
        verbose_name = 'раздел дисциплины'
        verbose_name_plural = 'разделы дисциплин'

    def __str__(self):
        return self.name


class DisciplineUser(models.Model):
    user = models.ForeignKey(user_model, on_delete=models.CASCADE, verbose_name='преподаватель')
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE, verbose_name='дисциплина')

    def __str__(self):
        return f'Преподаватель: {self.user}, дисциплина: {self.discipline}'


