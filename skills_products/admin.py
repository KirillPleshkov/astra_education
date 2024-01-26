from django.contrib import admin

from skills_products.models import Skill, Product


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ('name',)
