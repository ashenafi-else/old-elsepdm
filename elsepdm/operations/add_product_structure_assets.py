from elsecommon import marshalling
from elsepublic.elsepdm.dto.add_product_structure_assets import AddProductStructureAssetsParamsDTO
from elsepublic.elsepdm.serializers.add_product_structure_assets import AddProductStructureAssetsParamsSerializer
from elsepdm.models import (
    ProductStructure,
    ComponentAsset,
)
from elsepublic.exceptions import MissingProductStructureException

from elsepublic.elsedam.asset_extensions import AssetExtensions
from elsepublic.helpers.asset_dto_to_dict import asset_dto_to_dict


class AddProductStructureAssetsOperation(marshalling.ElseOperation):
    """
    Operation to add product structure assets

    Attributes
    ----------
    expect_serializer_class : elsepublic.elsepdm.serializers.add_product_structure_assets.AddProductStructureAssetsParamsSerializer
        Expect serializer.

    Raises
    ------
    MissingProductStructureException
        if structure with given uuid doesn't exist
    """
    expect_serializer_class = AddProductStructureAssetsParamsSerializer

    def __call__(self, data: AddProductStructureAssetsParamsDTO, **context) -> None:
        """
        Parameters
        ----------
        data : elsepublic.elsepdm.dto.add_product_structure_assets.AddProductStructureAssetsParamsDTO
            Operation input parameters
        context : dict
            context data

        Returns
        -------
        None
        """
        for structure_uuid, dam_asset in data.structures_mapping.items():
            structure = ProductStructure.objects.filter(uuid=structure_uuid).first()
            if not structure:
                raise MissingProductStructureException
            if dam_asset.extension == AssetExtensions.BLEND:
                asset_type = ComponentAsset.MODEL_ASSET
            else:
                asset_type = ComponentAsset.OBJ_ASSET
            ComponentAsset.objects.create(
                structure=structure,
                asset_type=asset_type,
                **asset_dto_to_dict(dam_asset),
            )
