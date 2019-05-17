from elsecommon import marshalling
from elsepdm.models import (
    ComponentAsset,
    ProductStructure,
)
from elsepublic.elsepdm.attach_geometry_assets import (
    AttachGeometryAssetsParams,
    AttachGeometryAssetsParamsSerializer,
)


@marshalling.async_marshall(expect=AttachGeometryAssetsParamsSerializer)
async def attach_geometry_operation(
        params: AttachGeometryAssetsParams,
        **context,
) -> None:
    """
    Operation which attach dam assets to structures

    Attributes
    ----------
    params:
        elsepublic.elsepdm.attach_geometry_assets.AttachGeometryAssetsParams
        Operation input params
    context: dict
        keyword arguments

    Returns
    -------
    None
    """
    component_assets = []
    for mapping in params.structures_mapping:
        structure = ProductStructure.objects.get(uuid=mapping.structure_uuid)
        for asset in mapping.assets:
            component_assets.append(ComponentAsset(
                asset_type=ComponentAsset.MODEL_ASSET,
                structure=structure,
                resource_type=mapping.batch.resource_type,
                dam_uuid=asset.dam_uuid,
                filename=asset.filename,
                size=asset.size,
                extension=asset.extension,
                brand_id=asset.brand_id,
                url=asset.url,
                state=asset.state,
                meta_info=asset.meta_info,
            ))

    ComponentAsset.objects.bulk_create(component_assets)
