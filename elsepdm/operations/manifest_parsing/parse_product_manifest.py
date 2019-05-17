from elsecommon import marshalling
from elsepublic.elsepdm.dto.parse_product_manifest import ParseProductManifestParamsDTO
from elsepublic.elsepdm.serializers.parse_product_manifest import ParseProductManifestParamsSerializer
from elsepdm.operations.manifest_parsing.manifest_parsing_utils import get_single_configuration_manifest_materials
from elsepdm.models import (
    ProductRevision,
    Material,
)
from elsepublic.exceptions import (
    MissingProductRevisionException,
    NotUpdatedRevisionException,
    MissingMaterialException,
)

from elsepdm.serializers import ProductComponentSerializer


class ParseProductManifestOperation(marshalling.ElseOperation):
    """
    Operation to parse product manifest

    Attributes
    ----------
    expect_serializer_class : elsepublic.elsepdm.serializers.parse_product_manifest.ParseProductManifestParamsSerializer
        Expect serializer.

    Raises
    ------
    MissingProductRevisionException
        if revision with given uuid doesn't exist
    NotUpdatedRevisionException
        if given revision is not updated
    MissingMaterialException
        if manifest contains missing materials
    """
    expect_serializer_class = ParseProductManifestParamsSerializer

    def __call__(self, data: ParseProductManifestParamsDTO, **context) -> None:
        """
        Parameters
        ----------
        data : elsepublic.elsepdm.dto.parse_product_manifest.ParseProductManifestParamsDTO
            Operation input parameters
        context : dict
            context data

        Returns
        -------
        None
        """
        revision = ProductRevision.objects.filter(uuid=data.revision_uuid).first()
        if not revision:
            raise MissingProductRevisionException

        if revision.state != ProductRevision.UPDATED:
            raise NotUpdatedRevisionException

        components = revision.json_configuration['config']['components']
        # materials = revision.json_configuration['config'].get('materials')
        #
        # materials = set(materials.keys()) if materials else get_single_configuration_manifest_materials(components)
        # saved_materials_amount = Material.objects.filter(
        #     collection=revision.product.collection,
        #     name__in=materials,
        # ).count()
        #
        # if saved_materials_amount != len(materials):
        #     raise MissingMaterialException

        for i, component in enumerate(components):
            product_component_serializer = ProductComponentSerializer(data=component)
            product_component_serializer.is_valid(raise_exception=True)
            product_component_serializer.save(product=revision, index=i)

        revision.state = ProductRevision.PARSED
        revision.save()
