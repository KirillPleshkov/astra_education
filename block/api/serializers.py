from rest_framework import serializers

from block.models import Block, BlockFiles


class BlockFilesSerializer(serializers.ModelSerializer):

    class Meta:
        model = BlockFiles
        fields = '__all__'


class BlockSerializer(serializers.ModelSerializer):
    files = BlockFilesSerializer(many=True)

    class Meta:
        model = Block
        fields = '__all__'




