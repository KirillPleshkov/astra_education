# Generated by Django 4.2.9 on 2024-01-26 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discipline', '0004_alter_discipline_name'),
        ('skills_products', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SkillCurriculum',
            new_name='SkillDiscipline',
        ),
        migrations.AlterField(
            model_name='skill',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='название'),
        ),
    ]