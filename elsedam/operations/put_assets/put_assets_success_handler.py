import logging

from elsecommon import marshalling
from elsepublic.dto.dam_asset_info import (
    DamAssetInfoDTO,
    DamAssetsInfoDTO,
)
from elsepublic.elsedam.put_assets.dto import PutAssetsResult
from elsepublic.serializers.dam_asset_info import DamAssetsInfoSerializer
from elsepublic.elsedam.put_assets.serializers import PutAssetsResultSerializer

logger = logging.getLogger()


class PutAssetsSuccessHandler(marshalling.ElseOperation):
    """
    Success handler for put assets. Convert PutAssetsResultSerializer to DamAssetsInfoDTO

    Attributes
    ----------
    expect_serializer_class : elsepublic.elsedam.serializers.put_assets_operation.PutAssetsResultSerializer
        Expect serializer.
    expose_serializer_class : elsepublic.serializers.dam_asset_info.DamAssetsInfoSerializer
        Expose serializer.
    """
    expect_serializer_class = PutAssetsResultSerializer
    expose_serializer_class = DamAssetsInfoSerializer

    def __call__(self, data: PutAssetsResult, **context) -> DamAssetsInfoDTO:
        """
        Parameters
        ----------
        data : elsepublic.elsedam.dto.put_assets_operation.PutAssetsResult
            Operation input parameters
        context : dict
            context data

        Returns
        -------
        elsepublic.dto.dam_asset_info.DamAssetsInfoDTO
        """
        dam_assets_info = []
        for dam_asset in data.dam_assets:
            dam_assets_info.append(
                DamAssetInfoDTO(
                    dam_uuid=dam_asset.uuid,
                    filename=dam_asset.filename,
                    size=dam_asset.size,
                    extension=dam_asset.extension,
                    brand_id=dam_asset.brand_id,
                    url=dam_asset.url,
                    state=dam_asset.state,
                    meta_info=dam_asset.meta_info,
                )
            )
        return DamAssetsInfoDTO(
            dam_assets_info=dam_assets_info,
            dam_asset_batch=data.dam_asset_batch,
        )
