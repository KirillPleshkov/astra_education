# Generated by Django 4.2.9 on 2024-01-15 15:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('block', '0003_block_module'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='block',
            options={'verbose_name': 'блок модуля', 'verbose_name_plural': 'блоки модулей'},
        ),
    ]
