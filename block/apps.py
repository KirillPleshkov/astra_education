from django.apps import AppConfig


class ModuleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'block'
    verbose_name = 'блоки модуля'
