from rest_framework import serializers

from discipline.models import Discipline
from module.api.serializers import ModuleNamesSerializer
from skills_products.api.serializers import SkillSerializer, ProductSerializer


class DisciplineSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)
    products = ProductSerializer(many=True, read_only=True)
    modules = ModuleNamesSerializer(many=True, read_only=True)

    class Meta:
        model = Discipline
        fields = ('name', 'short_description', 'skills', 'products', 'modules')
