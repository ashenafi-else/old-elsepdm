from .serializers import ProductComponentSerializer
from .serializers import ProductStructureSerializer
from .serializers import ProductElementSerializer


def create_components_structures(components, product_revision):
    for k, component in components.items():
        product_component_serializer = ProductComponentSerializer(data=component)
        product_component_serializer.is_valid(raise_exception=True)
        component_obj = product_component_serializer.save(product=product_revision)
        for i, structure in component['structures'].items():
            product_structure_serializer = ProductStructureSerializer(data=structure)
            product_structure_serializer.is_valid(raise_exception=True)
            structure_obj = product_structure_serializer.save(component=component_obj)
            for j, element in structure['elements'].items():
                product_element_serializer = ProductElementSerializer(data=element)
                product_element_serializer.is_valid(raise_exception=True)
                product_element_serializer.save(structure=structure_obj)

