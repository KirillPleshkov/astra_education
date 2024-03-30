from rest_framework import serializers

from block.api.serializers import BlockSerializer
from block.models import Block, BlockFiles
from module.models import Module


class ModuleNamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ('id', 'name')


class ModuleSerializer(serializers.ModelSerializer):
    blocks = BlockSerializer(many=True)

    class Meta:
        model = Module
        fields = '__all__'

    def create(self, validated_data):
        module_name = self.validated_data['name']
        return Module.objects.create(name=module_name)

    def _block_update_or_add(self, block_data, instance_id):
        block_id = block_data.get("id")

        if block_id:
            block_obj = Block.objects.get(id=block_id)
            block_obj.name = block_data.get("name")
            block_obj.main_text = block_data.get("main_text")
            block_obj.position = block_data.get("position")
            block_obj.save()
        else:
            block_obj = Block.objects.create(
                name=block_data.get("name"),
                main_text=block_data.get("main_text"),
                position=block_data.get("position"),
                module_id=instance_id
            )
        return block_obj

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)

        blocks_data = self.initial_data.get('blocks')
        new_block_list = []
        new_file_list = []

        for block_data in blocks_data:
            block_obj = self._block_update_or_add(block_data, instance.id)
            new_block_list.append(block_obj)
            instance.blocks.add(block_obj)

            files_data = block_data.get("files")
            for file_data in files_data:
                file_id = file_data.get("id")

                if not file_id:
                    continue

                file_obj = BlockFiles.objects.get(id=file_id)
                file_obj.position = file_data.get("position")
                file_obj.block = block_obj
                file_obj.is_saved = True
                file_obj.save()

                new_file_list.append(file_obj)

        current_module_blocks = Block.objects.filter(module_id=instance.id)

        for current_module_block in current_module_blocks:
            if not current_module_block in new_block_list:
                current_module_block.delete()

        current_module_files = BlockFiles.objects.filter(block__module_id=instance.id)

        for current_module_file in current_module_files:
            if not current_module_file in new_file_list:
                current_module_file.delete()

        instance.save()
        return instance
