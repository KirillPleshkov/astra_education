from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.utils.safestring import mark_safe

from discipline.models import Discipline, Section

from django.urls import reverse
from django.utils.http import urlencode

from module.models import Module


@admin.register(Discipline)
class DisciplineAdmin(admin.ModelAdmin):
    readonly_fields = ('get_list_sections',)
    fields = ('name', 'short_description', 'get_list_sections')

    add_fieldsets = (
        (None, {
            'description': None,
            'fields': ('name', 'short_description'),
        }),
    )

    def get_list_sections(self, obj):
        """Выводим список разделов со ссылками на соответствующие им блоки"""
        sections = set(Section.objects.filter(modules__discipline=obj))
        if not sections:
            return 'Разделы в данную дисциплину еще не добавили.'

        content_type = ContentType.objects.get_for_model(Module)
        section_html = '<p>'.join(
            [
                f'<a href="{reverse(f"admin:{content_type.app_label}_{content_type.model}_changelist") + "?" + urlencode({"discipline__id": obj.id, "section__id": section.id})}">{section.name}</a>'
                for
                section in sections])
        return mark_safe(section_html)

    get_list_sections.short_description = 'Разделы'

    def get_fieldsets(self, request, obj=None):
        """Убираем поле Разделы для страницы добавления дисциплины заменяя fieldsets"""
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    ...
