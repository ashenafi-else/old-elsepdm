from elsecommon import marshalling
from elsepdm.models import (
    ProductAsset,
    Configuration,
    ShoePairSettings,
)
from elsecommon.transports.router import Router
from elsepublic.elsepdm.shoe_pair import (
    MakeShoePairParams,
    MakeShoePairResult,
    MakeShoePairParamsSerializer,
    MakeShoePairResultSerializer,
)
from elsepublic.helpers.asset_to_dto import asset_to_dto
from elsepublic.elserender.mirroring_operation import (
    AsyncMirroringParams,
    AsyncMirroringOpInterface,
)


@marshalling.async_marshall(
    expect=MakeShoePairParamsSerializer,
    expose=MakeShoePairResultSerializer,
)
async def make_shoe_pair_operation(
        params: MakeShoePairParams,
        **context,
) -> MakeShoePairResult:
    """
    Operation which make shoe pair asset for configuration

    Attributes
    ----------
    params:
        elsepublic.elsepdm.shoe_pair.MakeShoePairParams
        Operation input params
    context: dict
        keyword arguments

    Returns
    -------
    MakeShoePairResult
    """
    configuration = Configuration.objects.get(pk=params.configuration_uuid)
    configuration_asset = configuration.assets.get(
        asset_type=ProductAsset.MODEL_ASSET,
    )
    pair_settings = ShoePairSettings.objects.get(pk=params.settings_uuid)
    mirror_params = AsyncMirroringParams(
        asset=asset_to_dto(configuration_asset),
        axes=pair_settings.axes,
        distance=pair_settings.distance,
        shouldnt_be_reflected=pair_settings.shouldnt_be_reflected,
    )
    mirror_op = Router[AsyncMirroringOpInterface]
    mirror_result = await mirror_op(mirror_params, **context)
    pair_asset = configuration.assets.create(
        asset_type=ProductAsset.PAIR_ASSET,
        resource_type=mirror_result.resource_type,
        dam_uuid=mirror_result.asset.dam_uuid,
        filename=mirror_result.asset.filename,
        size=mirror_result.asset.size,
        extension=mirror_result.asset.extension,
        brand_id=mirror_result.asset.brand_id,
        url=mirror_result.asset.url,
        state=mirror_result.asset.state,
        meta_info=mirror_result.asset.meta_info,
    )

    return MakeShoePairResult(
        asset_uuid=pair_asset.uuid,
    )
