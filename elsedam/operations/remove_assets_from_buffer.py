import logging
from azure.common import AzureException

from elsecommon.transports.router import Router
from elsecommon import marshalling
from elsepublic.elsedam.dto.remove_assets_from_buffer_operation import (
    RemoveAssetsFromBufferParameters,
    RemoveAssetsFromBufferResult,
)
from elsepublic.elsedam.serializers.remove_assets_from_buffer_operation import (
    RemoveAssetsFromBufferSerializer,
    RemoveAssetsFromBufferResultSerializer,
)
from elsepublic.elsedam.interfaces.remove_assets_operation import RemoveAssetsOpInterface
from elsepublic.elsedam.dto.remove_assets_operation import RemoveAssetsParameters
from ..models import (
    BufferedDamAsset,
    DamAsset,
    Storage,
)

logger = logging.getLogger()


class RemoveAssetsFromBufferOperation(marshalling.ElseOperation):
    """
    Operation for upload assets to buffer.

    Attributes
    ----------
    expect_serializer_class : elseserializers.BaseDtoSerializer
        Expect serializer.
    expose_serializer_class : elseserializers.BaseDtoSerializer
        Expose serializer.
    """
    expect_serializer_class = RemoveAssetsFromBufferSerializer
    expose_serializer_class = RemoveAssetsFromBufferResultSerializer

    def __call__(self, data: RemoveAssetsFromBufferParameters, **context) -> RemoveAssetsFromBufferResult:
        buffered_assets = BufferedDamAsset.objects.filter(for_removing=True)
        buf_storage = Storage.objects.filter(
            brand__is_default=True, storage_type=Storage.TYPE_BUFFERED).first().child_storage
        failed = []
        for buffered_asset in buffered_assets:
            try:
                buf_storage.delete(buffered_asset.buffer_path)
            except AzureException as err:
                logger.error(str(err))
                buffered_asset.meta_info = str(err)
                buffered_asset.state = BufferedDamAsset.FAILED_STATE
                buffered_asset.save()
                failed.append(buffered_asset.uuid)
        buffered_assets = buffered_assets.exclude(uuid__in=failed)
        dam_assets = DamAsset.objects.filter(buffered_asset__in=buffered_assets, temporary=True)
        buffered_assets.delete()

        remove_assets = Router[RemoveAssetsOpInterface.uri]

        remove_assets(RemoveAssetsParameters(dam_assets_uuids=[dam_asset.uuid for dam_asset in dam_assets]), **context)
        if failed:
            return RemoveAssetsFromBufferResult(success=False, failed_uuids=failed)
        return RemoveAssetsFromBufferResult(success=True, failed_uuids=[])
