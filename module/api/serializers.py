from rest_framework import serializers

from module.models import Module


class ModuleNamesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Module
        fields = ('pk', 'name')
