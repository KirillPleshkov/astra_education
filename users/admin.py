from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from users.forms import CustomUserCreationForm, CustomUserChangeForm
from users.models import Role

user_model = get_user_model()


@admin.register(user_model)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ('email', 'first_last_name', 'role', 'is_active',)
    list_filter = ('role', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Информация', {'fields': ('first_name', 'last_name', 'role')}),
        ('Права', {'fields': ('is_staff', 'is_active')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
         ),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

    def first_last_name(self, obj):
        return f'{obj.first_name} {obj.last_name}'

    first_last_name.short_description = 'Имя и фамилия'


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    ...


admin.site.unregister(Group)

