# Generated by Django 4.2.9 on 2024-01-15 14:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='название')),
                ('main_text', models.TextField(blank=True, default='', verbose_name='основной текст')),
                ('position', models.IntegerField(verbose_name='позиция')),
            ],
            options={
                'verbose_name': 'блок программы',
                'verbose_name_plural': 'блоки программ',
            },
        ),
        migrations.CreateModel(
            name='BlockFiles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='module_files/%Y/%m/%d/', verbose_name='файл')),
                ('position', models.IntegerField(verbose_name='позиция')),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='block.block', verbose_name='блок')),
            ],
            options={
                'verbose_name': 'файл блока',
                'verbose_name_plural': 'файлы блока',
            },
        ),
    ]
