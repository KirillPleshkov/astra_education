from django.contrib import admin
from django.contrib.auth import get_user_model

from discipline.models import Discipline, DisciplineModule
from block.models import Block
from skills_products.models import SkillDiscipline, ProductDiscipline

user_model = get_user_model()


class ModulesInline(admin.TabularInline):
    model = DisciplineModule
    autocomplete_fields = ('module',)
    ordering = ('position',)
    extra = 0


class SkillsInline(admin.TabularInline):
    model = SkillDiscipline
    autocomplete_fields = ('skill',)
    extra = 0


class ProductsInline(admin.TabularInline):
    model = ProductDiscipline
    autocomplete_fields = ('product',)
    extra = 0


@admin.register(Discipline)
class DisciplineAdmin(admin.ModelAdmin):
    fields = ('name', 'short_description')
    inlines = (ModulesInline, SkillsInline, ProductsInline)
    search_fields = ('name',)

    def get_inline_instances(self, request, obj=None):
        """Убираем inline при создании дисциплины"""
        return obj and super(DisciplineAdmin, self).get_inline_instances(request, obj) or []
