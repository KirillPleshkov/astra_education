from rest_framework import serializers, validators

from discipline.models import Discipline, DisciplineModule
from module.api.serializers import ModuleNamesSerializer
from module.models import Module
from skills_products.api.serializers import SkillSerializer, ProductSerializer
from skills_products.models import Product, Skill


class DisciplineElementSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)


class DisciplineModuleSerializer(serializers.ModelSerializer):
    module = DisciplineElementSerializer()

    class Meta:
        model = DisciplineModule
        fields = ('module', 'position')


class DisciplineSerializer(serializers.ModelSerializer):
    skills = DisciplineElementSerializer(many=True)
    products = DisciplineElementSerializer(many=True)
    modules = DisciplineModuleSerializer(many=True, source='disciplinemodule_set')

    class Meta:
        model = Discipline
        fields = '__all__'

    def update(self, instance, validated_data):

        instance.name = validated_data.get("name", instance.name)
        instance.short_description = validated_data.get("short_description", instance.short_description)

        products = []
        for product in validated_data.pop('products'):
            obj = Product.objects.get(id=product.get("id"), name=product.get("name"))
            products.append(obj)
        instance.products.set(products)

        skills = []
        for skill in validated_data.pop('skills'):
            obj = Skill.objects.get(id=skill.get("id"), name=skill.get("name"))
            skills.append(obj)
        instance.skills.set(skills)

        DisciplineModule.objects.filter(discipline_id=instance.id).delete()

        for module in validated_data.pop('disciplinemodule_set'):
            DisciplineModule.objects.create(position=module.get('position'),
                                            module_id=module.get('module').get('id'),
                                            discipline_id=instance.id)

        instance.save()
        return instance


class DisciplineNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discipline
        fields = ('name', 'id')
