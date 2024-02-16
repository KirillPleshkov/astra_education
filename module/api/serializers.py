from rest_framework import serializers

from block.api.serializers import BlockSerializer
from module.models import Module


class ModuleNamesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Module
        fields = ('pk', 'name')


class ModuleSerializer(serializers.ModelSerializer):
    blocks = BlockSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = '__all__'
