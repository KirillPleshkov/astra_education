from django.db import models

from discipline.models import Discipline


class EducationalLevel(models.Model):
    """Уровень образования (бакалавр, магистратура...)"""

    name = models.CharField(max_length=50, unique=True, verbose_name='название')
    study_period = models.IntegerField(verbose_name='срок обучения')

    class Meta:
        verbose_name = 'уровень образования'
        verbose_name_plural = 'уровни образования'

    def __str__(self):
        return self.name


class Curriculum(models.Model):
    """Учебный план"""

    name = models.CharField(max_length=100, unique=True, verbose_name='название')

    educational_level = models.ForeignKey(EducationalLevel, on_delete=models.PROTECT, related_name='curriculum',
                                          verbose_name='уровень обучения')
    disciplines = models.ManyToManyField(Discipline, through='CurriculumDiscipline', verbose_name='дисциплины',
                                         related_name='curriculums')

    class Meta:
        verbose_name = 'учебный план'
        verbose_name_plural = 'учебные планы'

    def __str__(self):
        return self.name


class CurriculumDiscipline(models.Model):
    """Связь многие ко многим между учебным планом и дисциплиной"""

    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE, verbose_name='учебный план')
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE, verbose_name='дисциплина')
    semester = models.IntegerField(verbose_name='семестр')

    class Meta:
        verbose_name = 'дисциплина учебного плана'
        verbose_name_plural = 'дисциплины учебного плана'
        unique_together = ('discipline', 'curriculum', 'semester')

    def __str__(self):
        return f'Учебный план: {self.curriculum.name}, дисциплина: {self.discipline.name}'
