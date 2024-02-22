from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from astra_education import settings
from curriculum.models import CurriculumDiscipline, CurriculumDisciplineUser
from user.forms import CustomUserCreationForm, CustomUserChangeForm
from user.models import Role, LinguistRole, LinguistRoleUser

user_model = get_user_model()


class DisciplinesInline(admin.TabularInline):
    model = CurriculumDisciplineUser
    extra = 0
    autocomplete_fields = ('curriculum_discipline',)


class LinguistRoleInline(admin.TabularInline):
    model = LinguistRoleUser
    extra = 0
    autocomplete_fields = ('linguist_role',)


@admin.register(user_model)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    list_display = ('email', 'first_last_name', 'role', 'is_active',)
    list_filter = ('role', 'is_staff', 'is_active',)

    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

    inlines = (LinguistRoleInline, DisciplinesInline)

    def get_inline_instances(self, request, obj=None):
        if not obj or obj.role.name == settings.STUDENT_NAME:
            return []
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Информация', {'fields': ('first_name', 'last_name', 'role')}),
        ('Права', {'fields': ('is_staff', 'is_active')}),
        ('Учебный план', {'fields': ('curriculum',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
         ),
    )

    def first_last_name(self, obj):
        return f'{obj.first_name} {obj.last_name}'

    first_last_name.short_description = 'Имя и фамилия'


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    ...


@admin.register(LinguistRole)
class LinguistRoleAdmin(admin.ModelAdmin):
    search_fields = ('name',)


admin.site.unregister(Group)

