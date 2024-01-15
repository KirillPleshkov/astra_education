from django.db import models
from django.db.models import UniqueConstraint

from discipline.models import Discipline
from module.models import Module


class BlockFiles(models.Model):
    """Файлы привязанные к конкретному блоку"""

    file = models.FileField(upload_to='module_files/%Y/%m/%d/', verbose_name='файл')
    position = models.IntegerField(verbose_name='позиция')

    block = models.ForeignKey('Block', on_delete=models.CASCADE, related_name='files', verbose_name='блок')

    class Meta:
        verbose_name = 'файл блока'
        verbose_name_plural = 'файлы блока'

    def __str__(self):
        return self.file.name.split('/')[-1]


class Block(models.Model):
    """Блок конкретной дисциплины и раздела этой дисциплины"""

    name = models.CharField(max_length=50, verbose_name='название')
    main_text = models.TextField(blank=True, default='', verbose_name='основной текст')
    position = models.IntegerField(verbose_name='позиция')

    module = models.ForeignKey(Module, on_delete=models.CASCADE, verbose_name='модуль', related_name='blocks')

    class Meta:
        verbose_name = 'блок модуля'
        verbose_name_plural = 'блоки модуля'

    def __str__(self):
        return self.name
