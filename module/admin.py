from django.contrib import admin

from block.models import Block
from module.models import Module


class BlocksInline(admin.TabularInline):
    model = Block
    extra = 0
    fields = ('name', 'position')
    exclude = ('main_text',)
    readonly_fields = ('name',)
    ordering = ('position',)
    show_change_link = True

    def has_add_permission(self, request, obj):
        """Убираем возможность добавить запись в inline"""
        return False


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    inlines = (BlocksInline,)

    def get_inline_instances(self, request, obj=None):
        """Убираем inline при создании дисциплины"""
        return obj and super(ModuleAdmin, self).get_inline_instances(request, obj) or []

