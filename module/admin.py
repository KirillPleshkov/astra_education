from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.safestring import mark_safe
from discipline.models import Discipline
from module.models import Module, ModuleFiles


class ModuleFilesInline(admin.TabularInline):
    model = ModuleFiles
    extra = 0
    readonly_fields = ('__str__',)
    fields = ('__str__', 'position')
    show_change_link = True

    def has_add_permission(self, request, obj):
        """Убираем возможность добавить запись в inline"""
        return False


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'section', 'get_discipline_url')
    list_display_links = ('name',)
    inlines = [ModuleFilesInline]
    list_select_related = True
    search_fields = ('name', 'section__name', 'discipline__name')
    ordering = ('discipline', 'section')

    def get_discipline_url(self, obj):
        """Выводим название дисциплины к которой привязан блок со ссылкой на него"""
        discipline = Discipline.objects.get(modules=obj)
        content_type = ContentType.objects.get_for_model(discipline)
        url = reverse(f'admin:{content_type.app_label}_{content_type.model}_changelist') + "?" + urlencode(
            {"modules__id": f"{obj.id}"})
        return mark_safe(f'<a href="{url}">{discipline.name}</a>')

    get_discipline_url.short_description = 'дисциплина'

    def get_inline_instances(self, request, obj=None):
        """Убираем inline при создании блока"""
        return obj and super(ModuleAdmin, self).get_inline_instances(request, obj) or []


@admin.register(ModuleFiles)
class ModuleFilesAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'get_module_url')
    list_display_links = ('__str__',)
    search_fields = ('file', 'module__name')
    fields = ('file', 'position', 'module')

    def get_module_url(self, obj):
        """Выводим название блока к которому привязан файл со ссылкой на него"""
        module = Module.objects.get(files=obj)
        content_type = ContentType.objects.get_for_model(module)
        url = reverse(f'admin:{content_type.app_label}_{content_type.model}_changelist') + "?" + urlencode(
            {"files__id": f"{obj.id}"})
        return mark_safe(f'<a href="{url}">{module.name}</a>')

    get_module_url.short_description = 'блок'
