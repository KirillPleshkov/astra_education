from rest_framework import serializers, validators

from discipline.models import Discipline, DisciplineModule
from module.api.serializers import ModuleNamesSerializer
from skills_products.api.serializers import SkillSerializer, ProductSerializer
from skills_products.models import Product


class DisciplineModuleSerializer(serializers.ModelSerializer):
    module = ModuleNamesSerializer(read_only=True)

    class Meta:
        model = DisciplineModule
        fields = ('module', 'position')


class DisciplineSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)
    products = ProductSerializer(many=True)
    modules = DisciplineModuleSerializer(many=True, read_only=True, source='disciplinemodule_set')

    class Meta:
        model = Discipline
        fields = ('id', 'name', 'short_description', 'skills', 'products', 'modules')

    def update(self, instance, validated_data):
        print(1111)

        instance.name = validated_data.get("name", instance.name)
        instance.short_description = validated_data.get("short_description", instance.short_description)

        products = []
        for product in validated_data.get('products'):
            obj, _ = Product.objects.get(id=product.id)
            products.append(obj)
        instance.products.set(products)

        instance.save()
        return instance


class DisciplineNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discipline
        fields = ('name', 'id')
