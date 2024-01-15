from django.contrib.auth import get_user_model
from django.db import models

from module.models import Module

user_model = get_user_model()


class Discipline(models.Model):
    """Рабочие программы дисциплин"""

    name = models.CharField(max_length=50, verbose_name='название')
    short_description = models.TextField(blank=True, default='', max_length=500, verbose_name='краткое описание')

    modules = models.ManyToManyField(Module, through='DisciplineModule', related_name='disciplines')

    class Meta:
        verbose_name = 'дисциплина'
        verbose_name_plural = 'дисциплины'

    def __str__(self):
        return self.name


class DisciplineModule(models.Model):
    """Связь многие ко многим дисциплины и учебного модуля"""

    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE, verbose_name='дисциплина')
    module = models.ForeignKey(Module, on_delete=models.CASCADE, verbose_name='модуль')

    class Meta:
        verbose_name = 'модуль дисциплины'
        verbose_name_plural = 'модули дисциплины'
        unique_together = ('discipline', 'module')

    def __str__(self):
        return f'Дисциплина: {self.discipline.name}, модуль: {self.module.name}'
