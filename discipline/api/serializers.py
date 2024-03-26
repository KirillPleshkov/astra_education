from rest_framework import serializers

from discipline.models import Discipline, DisciplineModule
from module.api.serializers import ModuleNamesSerializer
from skills_products.api.serializers import SkillSerializer, ProductSerializer


class DisciplineModuleSerializer(serializers.ModelSerializer):
    module = ModuleNamesSerializer(read_only=True)

    class Meta:
        model = DisciplineModule
        fields = ('module', 'position')


class DisciplineSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)
    products = ProductSerializer(many=True, read_only=True)
    modules = DisciplineModuleSerializer(many=True, read_only=True, source='disciplinemodule_set')

    class Meta:
        model = Discipline
        fields = ('id', 'name', 'short_description', 'skills', 'products', 'modules')


class DisciplineNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discipline
        fields = ('name', 'id')
