from rest_framework import serializers

from block.models import Block, BlockFiles


class BlockFilesSerializer(serializers.ModelSerializer):

    class Meta:
        model = BlockFiles
        fields = '__all__'


class BlockFilesToUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = BlockFiles
        fields = '__all__'
        read_only_fields = ('file',)


class BlockSerializer(serializers.ModelSerializer):
    files = BlockFilesToUpdateSerializer(many=True)

    class Meta:
        model = Block
        fields = '__all__'




