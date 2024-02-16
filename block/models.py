from pytils import translit
from django.db import models
from django.db.models import UniqueConstraint
from pytz import unicode

from discipline.models import Discipline
from module.models import Module

import unicodedata
import re

from pytils.translit import slugify


def unique_slugify(slug):
    return '.'.join([slugify(el) for el in slug.split('.')])


def path_and_rename(path):
    def get_file_path(instance, filename):
        full_path = ''.join([path, unique_slugify(filename)])
        return full_path

    return get_file_path


class BlockFiles(models.Model):
    """Файлы привязанные к конкретному блоку"""

    file = models.FileField(upload_to=path_and_rename('module_files/%Y/%m/%d/'), verbose_name='файл')
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
