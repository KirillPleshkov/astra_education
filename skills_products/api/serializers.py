from rest_framework import serializers

from skills_products.models import Skill, Product


class SkillSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skill
        fields = ('id', 'name')


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('id', 'name')
