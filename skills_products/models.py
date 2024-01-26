from django.db import models

from discipline.models import Discipline


class Skill(models.Model):
    """Навыки полученные по прохождению дисциплины"""

    name = models.CharField(max_length=100, unique=True, verbose_name='название')

    disciplines = models.ManyToManyField(Discipline, through='SkillDiscipline', verbose_name='дисциплины',
                                         related_name='skills')

    class Meta:
        verbose_name = 'навык'
        verbose_name_plural = 'навыки'

    def __str__(self):
        return self.name


class SkillDiscipline(models.Model):
    """Связь многие ко многим между навыком и дисциплиной"""

    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, verbose_name='навык')
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE, verbose_name='дисциплина')

    class Meta:
        verbose_name = 'навык дисциплины'
        verbose_name_plural = 'навыки дисциплины'
        unique_together = ('skill', 'discipline')

    def __str__(self):
        return f'Навык: {self.skill.name}, дисциплина: {self.discipline.name}'


class Product(models.Model):
    """Изученные продукты ПАО Группа Астра по прохождению дисциплины"""

    name = models.CharField(max_length=100, unique=True, verbose_name='название')

    disciplines = models.ManyToManyField(Discipline, through='ProductDiscipline', verbose_name='дисциплины',
                                         related_name='products')

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'

    def __str__(self):
        return self.name


class ProductDiscipline(models.Model):
    """Связь многие ко многим между продуктом и дисциплиной"""

    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='продукт')
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE, verbose_name='дисциплина')

    class Meta:
        verbose_name = 'продукт дисциплины'
        verbose_name_plural = 'продукты дисциплины'
        unique_together = ('product', 'discipline')

    def __str__(self):
        return f'Продукт: {self.product.name}, дисциплина: {self.discipline.name}'
