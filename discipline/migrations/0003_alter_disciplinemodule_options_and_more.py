# Generated by Django 4.2.9 on 2024-01-15 16:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('module', '0002_alter_module_options'),
        ('discipline', '0002_disciplinemodule_discipline_modules'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='disciplinemodule',
            options={'verbose_name': 'модуль дисциплины', 'verbose_name_plural': 'модули дисциплины'},
        ),
        migrations.AlterField(
            model_name='disciplinemodule',
            name='discipline',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='discipline.discipline', verbose_name='дисциплина'),
        ),
        migrations.AlterField(
            model_name='disciplinemodule',
            name='module',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='module.module', verbose_name='модуль'),
        ),
        migrations.AlterUniqueTogether(
            name='disciplinemodule',
            unique_together={('discipline', 'module')},
        ),
    ]