from elsecommon import marshalling
from elsepdm.models import (
    ComponentAsset,
    ProductStructure,
)
from elsepublic.elsedam.put_assets.dto import PutAssetsResult
from elsepublic.elsedam.put_assets.serializers import PutAssetsResultSerializer


class ImportStructureFromObjSuccessHandler(marshalling.ElseOperation):
    """
    Handler for operation to import from obj file

    Attributes
    ----------
    expect_serializer_class : elsepublic.elsedam.serializers.put_assets_operation.PutAssetsResultSerializer
        Expect serializer.
    """
    expect_serializer_class = PutAssetsResultSerializer

    def __call__(self, data: PutAssetsResult, **context) -> None:
        """
        Parameters
        ----------
        data : elsepublic.elsedam.dto.put_assets_operation.PutAssetsResult
            Operation input parameters
        context : dict
            context data {structure_uuid}

        Returns
        -------
        None
        """
        structure = ProductStructure.objects.filter(
            uuid=context.pop('structure_uuid')).first()
        ComponentAsset.objects.create(
            asset_type=ComponentAsset.MODEL_ASSET,
            structure=structure,
            resource_type=data.dam_asset_batch.resource_type,
            dam_uuid=data.dam_assets[0].uuid,
            filename=data.dam_assets[0].filename,
            size=data.dam_assets[0].size,
            extension=data.dam_assets[0].extension,
            brand_id=data.dam_assets[0].brand_id,
            url=data.dam_assets[0].url,
            state=data.dam_assets[0].state,
            meta_info=data.dam_assets[0].meta_info,
        )
