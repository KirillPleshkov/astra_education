from django.db import models


class Module(models.Model):
    """Учебный модуль"""

    name = models.CharField(max_length=100, unique=True, verbose_name='название')

    class Meta:
        verbose_name = 'модуль'
        verbose_name_plural = 'модули'

    def __str__(self):
        return self.name
