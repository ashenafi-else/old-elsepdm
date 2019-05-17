import logging

from elsecommon import marshalling
from django.conf import settings
from azure.common import AzureException
from elsedam.models import (
    Storage,
    DamAsset,
    DamAssetRequest,
    BufferedDamAsset,
)
from elsepublic.elsedam.buffering_assets import (
    PutAssetToBufferResult,
    PutAssetsToBufferParams,
    PutAssetsToBufferResult,
    BufferedDamAssetParameters,
    PutAssetsToBufferSerializer,
    PutAssetsToBufferResultSerializer,
)

logger = logging.getLogger()


class AsyncPutAssetsToBufferOperation(marshalling.AsyncElseOperation):
    """
    Operation for upload assets to buffer.

    Attributes
    ----------
    expect_serializer_class:
        elsepublic.elsedam.buffering_assets.PutAssetsToBufferSerializer
        Expect serializer.
    expose_serializer_class:
        elsepublic.elsedam.buffering_assets.PutAssetsToBufferResultSerializer
        Expose serializer.
    """
    expect_serializer_class = PutAssetsToBufferSerializer
    expose_serializer_class = PutAssetsToBufferResultSerializer

    async def __call__(
            self,
            data: PutAssetsToBufferParams,
            **context,
    ) -> PutAssetsToBufferResult:
        storage = Storage.objects.filter(
            brand__is_default=True,
            storage_type=Storage.TYPE_BUFFERED).first().child_storage
        location = storage.locations.first()
        dam_asset_requests = []
        for uuid in data.dam_asset_uuids:
            buffered_asset = BufferedDamAsset.objects.filter(
                dam_asset__uuid=uuid).first()
            if buffered_asset:
                buffered_asset.for_removing = False
            else:
                asset = DamAsset.objects.get(uuid=uuid)
                buffered_asset = BufferedDamAsset.objects.create(
                    location=location, dam_asset=asset)
                path = storage.generate_path(asset)
                try:
                    storage.put_by_url(path, asset.url)
                except AzureException as err:
                    logger.error(str(err))
                    buffered_asset.state = BufferedDamAsset.FAILED_STATE
                    buffered_asset.meta_info = str(err)
                else:
                    buffered_asset.state = BufferedDamAsset.BUFFERED_STATE
                    buffered_asset.buffer_url = storage.generate_url(asset)
                    buffered_asset.buffer_path = path
            buffered_asset.save()

            dam_asset_request = DamAssetRequest(buffered_asset=buffered_asset)
            dam_asset_requests.append(dam_asset_request)
        created_requests = DamAssetRequest.objects.bulk_create(
            dam_asset_requests)
        dto_requests = [
            PutAssetToBufferResult(
                uuid=request.uuid,
                created=request.created,
                buffered_asset=BufferedDamAssetParameters(
                    uuid=request.buffered_asset.uuid,
                    buffer_url=request.buffered_asset.buffer_url,
                    buffer_path=request.buffered_asset.buffer_path,
                    buffer_file=settings.BUFFER_SERVICE.open_buffer_file(
                        request.buffered_asset.buffer_path),
                    state=request.buffered_asset.state,
                    meta_info=request.buffered_asset.meta_info,
                )) for request in created_requests]
        return PutAssetsToBufferResult(dam_asset_requests=dto_requests)
