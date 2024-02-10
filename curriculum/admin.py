from django.contrib import admin

from curriculum.models import Curriculum, EducationalLevel, CurriculumDiscipline


class DisciplinesInline(admin.TabularInline):
    model = CurriculumDiscipline
    extra = 0
    autocomplete_fields = ('discipline',)
    ordering = ('semester', 'discipline')


@admin.register(Curriculum)
class CurriculumAdmin(admin.ModelAdmin):
    inlines = (DisciplinesInline,)


@admin.register(EducationalLevel)
class EducationalLevelAdmin(admin.ModelAdmin):
    ...



