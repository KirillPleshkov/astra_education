from django.contrib import admin
from django.contrib.auth import get_user_model

from discipline.models import Discipline, DisciplineModule
from block.models import Block

user_model = get_user_model()


class ModulesInline(admin.TabularInline):
    model = DisciplineModule
    # exclude = ('main_text',)
    # readonly_fields = ('name', 'section')
    # ordering = ('section', 'position')
    # show_change_link = True
    # fields = ('name', 'section', 'position')
    autocomplete_fields = ('module',)
    extra = 0

    # def has_add_permission(self, request, obj):
    #     """Убираем возможность добавить запись в inline"""
    #     return False

#
# class TeachersInline(admin.TabularInline):
#     model = DisciplineUser
#     extra = 0
#     autocomplete_fields = ('user',)
#     verbose_name = 'преподаватель'
#     verbose_name_plural = 'преподаватели'


@admin.register(Discipline)
class DisciplineAdmin(admin.ModelAdmin):
    fields = ('name', 'short_description')
    inlines = (ModulesInline, )
    search_fields = ('name',)

    def get_inline_instances(self, request, obj=None):
        """Убираем inline при создании дисциплины"""
        return obj and super(DisciplineAdmin, self).get_inline_instances(request, obj) or []
