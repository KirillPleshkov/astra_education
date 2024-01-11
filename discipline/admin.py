from django.contrib import admin
from django.contrib.auth import get_user_model

from discipline.models import Discipline, Section
from module.models import Module

user_model = get_user_model()


class ModulesInline(admin.TabularInline):
    model = Module
    exclude = ('main_text',)
    readonly_fields = ('name', 'section')
    ordering = ('section', 'position')
    show_change_link = True
    fields = ('name', 'section', 'position')
    extra = 0

    def has_add_permission(self, request, obj):
        """Убираем возможность добавить запись в inline"""
        return False


class TeachersInline(admin.TabularInline):
    model = user_model.disciplines.through
    extra = 0


@admin.register(Discipline)
class DisciplineAdmin(admin.ModelAdmin):
    fields = ('name', 'short_description')
    inlines = (ModulesInline, TeachersInline)
    search_fields = ('name',)

    def get_inline_instances(self, request, obj=None):
        """Убираем inline при создании дисциплины"""
        return obj and super(DisciplineAdmin, self).get_inline_instances(request, obj) or []


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    search_fields = ('name',)
