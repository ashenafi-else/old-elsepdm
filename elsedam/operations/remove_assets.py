import logging
from azure.common import AzureException

from elsecommon import marshalling
from elsedam.models import DamAsset
from elsepublic.elsedam.dto.remove_assets_operation import (
    RemoveAssetsResult,
    RemoveAssetsParameters,
)
from elsepublic.elsedam.serializers.remove_assets_operation import (
    RemoveAssetsSerializer,
    RemoveAssetsResultSerializer,
)


logger = logging.getLogger()


class RemoveAssetsOperation(marshalling.ElseOperation):
    """
    Operation for remove asset from storage.

    Attributes
    ----------
    expect_serializer_class : elseserializers.BaseDtoSerializer
        Expect serializer.
    expose_serializer_class : elseserializers.BaseDtoSerializer
        Expose serializer.
    """
    expect_serializer_class = RemoveAssetsSerializer
    expose_serializer_class = RemoveAssetsResultSerializer

    def __call__(self, data: RemoveAssetsParameters, **context) -> RemoveAssetsResult:
        dam_assets = DamAsset.objects.filter(uuid__in=data.dam_assets_uuids)
        failed = []
        for dam_asset in dam_assets:
            storage = dam_asset.location.storage.child_storage
            path = storage.generate_path(dam_asset)
            try:
                storage.remove(path)
            except AzureException as err:
                logger.error(str(err))
                dam_asset.meta_info = str(err)
                dam_asset.state = DamAsset.FAILED_REMOVE_STATE
                dam_asset.save()
                failed.append(dam_asset.uuid)
        dam_assets = dam_assets.exclude(uuid__in=failed)
        dam_assets.delete()
        if failed:
            return RemoveAssetsResult(success=False, failed_uuids=failed)
        return RemoveAssetsResult(success=True, failed_uuids=[])
