from rest_framework import serializers

from block.api.serializers import BlockSerializer
from block.models import Block, BlockFiles
from module.models import Module


class ModuleNamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ('pk', 'name')


class ModuleSerializer(serializers.ModelSerializer):
    blocks = BlockSerializer(many=True)

    class Meta:
        model = Module
        fields = '__all__'

    # def update(self, instance, validated_data):
    #     instance.name = validated_data.get("name", instance.name)
    #
    #     blocks_data = self.initial_data.get('blocks')
    #     new_block_list = []
    #
    #     for block_data in blocks_data:
    #         block_id = block_data.get("id")
    #         if block_id:
    #             block_obj = Block.objects.get(id=block_id)
    #             block_obj.name = block_data.get("name")
    #             block_obj.main_text = block_data.get("main_text")
    #             block_obj.position = block_data.get("position")
    #             block_obj.save()
    #         else:
    #             block_obj = Block.objects.create(
    #                 name=block_data.get("name"),
    #                 main_text=block_data.get("main_text"),
    #                 position=block_data.get("position"),
    #                 module_id=instance.id
    #             )
    #         new_block_list.append(block_obj)
    #         instance.blocks.add(block_obj)
    #
    #     current_module_blocks = Block.objects.filter(module_id=instance.id)
    #
    #     for current_module_block in current_module_blocks:
    #         if not current_module_block in new_block_list:
    #             current_module_block.delete()
    #
    #     instance.save()
    #     return instance

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)

        blocks_data = self.initial_data.get('blocks')
        new_block_list = []

        for block_data in blocks_data:
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
                    module_id=instance.id
                )
            new_block_list.append(block_obj)
            instance.blocks.add(block_obj)

        current_module_blocks = Block.objects.filter(module_id=instance.id)

        for current_module_block in current_module_blocks:
            if not current_module_block in new_block_list:
                current_module_block.delete()

        instance.save()
        return instance
