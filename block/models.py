from django.db import models
from django.utils.deconstruct import deconstructible
from rest_framework.reverse import reverse

from discipline.models import Discipline
from module.models import Module

from pytils.translit import slugify


def unique_slugify(slug):
    return '.'.join([slugify(el) for el in slug.split('.')])


@deconstructible
class PathRename(object):

    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        full_path = ''.join([self.path, unique_slugify(filename)])
        return full_path


path_and_rename = PathRename("module_files/%Y/%m/%d/")


class BlockFiles(models.Model):
    """Файлы привязанные к конкретному блоку"""

    file = models.FileField(upload_to=path_and_rename, verbose_name='файл')
    position = models.IntegerField(verbose_name='позиция')
    is_saved = models.BooleanField(verbose_name='Сохранен', default=False)

    block = models.ForeignKey('Block', on_delete=models.CASCADE, related_name='files', verbose_name='блок', null=True,
                              blank=True)

    class Meta:
        verbose_name = 'файл блока'
        verbose_name_plural = 'файлы блока'

    def __str__(self):
        return self.file.name.split('/')[-1]

    def get_absolute_url(self):
        return reverse('block:file_download', kwargs={'pk': self.pk})

    def get_name(self):
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
