from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.safestring import mark_safe
from discipline.models import Discipline
from module.models import Module, ModuleFiles, Section


class ModuleFilesInline(admin.TabularInline):
    model = ModuleFiles
    extra = 1


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'section', 'get_discipline_url', 'position')
    list_display_links = ('name',)
    inlines = [ModuleFilesInline]
    list_select_related = True
    search_fields = ('name', 'section__name', 'discipline__name')
    ordering = ('position',)

    def get_discipline_url(self, obj):
        """Выводим название дисциплины к которой привязан блок со ссылкой на него"""
        discipline = Discipline.objects.get(modules=obj)
        content_type = ContentType.objects.get_for_model(discipline)
        url = reverse(f'admin:{content_type.app_label}_{content_type.model}_changelist') + "?" + urlencode(
            {"modules__id": f"{obj.id}"})
        return mark_safe(f'<a href="{url}">{discipline.name}</a>')

    get_discipline_url.short_description = 'дисциплина'


@admin.register(ModuleFiles)
class ModuleFilesAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'get_module_url')
    list_display_links = ('__str__',)
    search_fields = ('file', 'module__name')

    def get_module_url(self, obj):
        """Выводим название блока к которому привязан файл со ссылкой на него"""
        module = Module.objects.get(files=obj)
        content_type = ContentType.objects.get_for_model(module)
        url = reverse(f'admin:{content_type.app_label}_{content_type.model}_changelist') + "?" + urlencode(
            {"files__id": f"{obj.id}"})
        return mark_safe(f'<a href="{url}">{module.name}</a>')

    get_module_url.short_description = 'блок'
