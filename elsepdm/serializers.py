from rest_framework import serializers

from elsepdm.models import (
    ProductComponent,
    ProductStructure,
    ProductElement,
)


class ProductElementSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False, max_length=64)
    materials = serializers.ListField(child=serializers.CharField(), required=False)

    def create(self, validated_data):
        return ProductElement.objects.create(
            active_material=validated_data['active_material'],
            active_color=validated_data['active_color'],
            path=validated_data['path'],
            name=validated_data.get('name', validated_data['path']),
            element=validated_data['element'],
            configurable=validated_data.get('configurable', True),
            materials=validated_data.get('materials', []),
            structure=validated_data['structure'],
        )

    class Meta:
        model = ProductElement
        exclude = ('structure',)


class ProductStructureSerializer(serializers.ModelSerializer):
    elements = ProductElementSerializer(many=True)

    def create(self, validated_data):
        data = {**validated_data}
        elements = data.pop('elements')
        structure = ProductStructure.objects.create(**data)

        for i, element in enumerate(elements):
            product_element_serializer = ProductElementSerializer(data=element)
            product_element_serializer.is_valid(raise_exception=True)
            product_element_serializer.save(structure=structure)

        return structure

    class Meta:
        model = ProductStructure
        exclude = ('component', 'export_name',)


class ProductComponentSerializer(serializers.ModelSerializer):
    structures = ProductStructureSerializer(many=True)
    order = serializers.IntegerField(required=False)

    def create(self, validated_data):
        data = {**validated_data}
        structures = data.pop('structures')
        index = data.pop('index')

        if 'order' not in validated_data:
            data['order'] = index
        component = ProductComponent.objects.create(**data)

        for i, structure in enumerate(structures):
            product_structure_serializer = ProductStructureSerializer(data=structure)
            product_structure_serializer.is_valid(raise_exception=True)
            product_structure_serializer.save(component=component)

        return component

    class Meta:
        model = ProductComponent
        exclude = ('product',)


class ProductConfigSerializer(serializers.Serializer):
    components = ProductComponentSerializer(many=True)
    materials = serializers.DictField(child=serializers.ListField(child=serializers.CharField()), required=False)
    default_configuration_path = serializers.CharField(required=False)
    available_configurations = serializers.ListField(child=serializers.DictField(child=serializers.CharField()),
                                                     required=False)


class ProductManifestSerializer(serializers.Serializer):
    product = serializers.CharField()
    config = ProductConfigSerializer()



