from django.db import models


class Discipline(models.Model):
    """Дисциплина"""

    name = models.CharField(max_length=50, verbose_name='название')
    short_description = models.TextField(blank=True, default='', max_length=500, verbose_name='краткое описание')

    class Meta:
        verbose_name = 'дисциплина'
        verbose_name_plural = 'дисциплины'

    def __str__(self):
        return self.name


class Section(models.Model):
    """Раздел дисциплины"""

    name = models.CharField(max_length=50, verbose_name='название')

    class Meta:
        verbose_name = 'раздел дисциплины'
        verbose_name_plural = 'разделы дисциплин'

    def __str__(self):
        return self.name
