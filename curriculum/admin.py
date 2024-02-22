from django.contrib import admin

from curriculum.models import Curriculum, EducationalLevel, CurriculumDiscipline, CurriculumDisciplineUser


class DisciplinesInline(admin.TabularInline):
    model = CurriculumDiscipline
    extra = 0
    autocomplete_fields = ('discipline',)
    ordering = ('semester', 'discipline')


@admin.register(Curriculum)
class CurriculumAdmin(admin.ModelAdmin):
    inlines = (DisciplinesInline,)
    search_fields = ('name',)


@admin.register(EducationalLevel)
class EducationalLevelAdmin(admin.ModelAdmin):
    ...


class UsersInline(admin.TabularInline):
    model = CurriculumDisciplineUser
    extra = 0
    autocomplete_fields = ('user',)


@admin.register(CurriculumDiscipline)
class CurriculumDisciplineAdmin(admin.ModelAdmin):
    inlines = (UsersInline,)
    autocomplete_fields = ('discipline', 'curriculum')
    search_fields = ('discipline__name', 'curriculum__name')
