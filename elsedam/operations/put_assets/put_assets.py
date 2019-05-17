import os
import shutil
import logging
import mimetypes

from elsecommon import marshalling
from azure.common import AzureException
from elsedam.models import (
    DamAsset,
    DamAssetBatch,
)
from elsepublic.elsedam.put_assets import (
    PutAssetResult,
    PutAssetsParams,
    PutAssetsResult,
    DamAssetBatchDTO,
    PutAssetsParamsSerializer,
    PutAssetsResultSerializer,
)
from elsedam.operations.helpers.get_storage_group import get_storage_group

logger = logging.getLogger()


class PutAssetsOperation(marshalling.ElseOperation):
    """
    Operation for upload assets to storage.
    Get dto with a list of assets, create
    dam asset and put assets files to the
    storage according to the tags and brands ids.
    Return dto with a list of dam assets

    Attributes
    ----------
    expect_serializer_class:
        elsepublic.elsedam.put_assets.PutAssetsParamsSerializer
        Expect serializer.
    expose_serializer_class:
        elsepublic.elsedam.put_assets.PutAssetsResultSerializer
        Expose serializer.
    """
    expect_serializer_class = PutAssetsParamsSerializer
    expose_serializer_class = PutAssetsResultSerializer

    def __call__(self, data: PutAssetsParams, **context) -> PutAssetsResult:
        """
        Parameters
        ----------
        data : elsepublic.elsedam.dto.put_assets_operation.PutAssetsParams
            Operation input parameters
        context : dict
            context data

        Returns
        -------
        elsepublic.elsedam.dto.put_assets_operation.PutAssetsResult
        """
        criteria_group_map = {}
        dam_assets = []
        assets_dir = None
        batch = DamAssetBatch.objects.create(
            resource_type=data.resource_type,
            initiator=data.initiator,
            description=data.description,
        )
        for base_asset in data.base_assets:
            if not assets_dir:
                assets_dir = os.path.dirname(base_asset.file.name)
            criteria = (base_asset.brand_id, tuple(sorted(base_asset.tags)))
            storage_group = criteria_group_map.get(criteria)
            mime_type, _ = mimetypes.guess_type(base_asset.file.name)
            if not mime_type:
                mime_type = 'application/octet-stream'
            if not storage_group:
                storage_group = get_storage_group(base_asset)
            criteria_group_map[criteria] = storage_group
            filename, extension = os.path.splitext(base_asset.filename)
            size = os.path.getsize(base_asset.file.name)
            dam_asset = DamAsset.objects.create(
                batch=batch,
                filename=filename,
                extension=extension,
                tags=base_asset.tags,
                brand_id=base_asset.brand_id,
                group=storage_group,
                size=size,
                mime_type=mime_type,
                state=DamAsset.UPLOADING_STATE,
                location=storage_group.location,
                relative_path=base_asset.relative_path,
            )
            storage = storage_group.location.storage.child_storage
            path = storage.generate_path(dam_asset)
            try:
                storage.put_by_stream(path, base_asset.file, mime_type)
            except AzureException as err:
                logger.error(str(err))
                dam_asset.meta_info = str(err)
                dam_asset.state = DamAsset.FAILED_STATE
            else:
                dam_asset.state = DamAsset.UPLOADED_STATE
                dam_asset.url = storage.generate_url(dam_asset)
            dam_asset.save()
            dam_assets.append(PutAssetResult(
                uuid=dam_asset.uuid,
                filename=dam_asset.filename,
                size=dam_asset.size,
                mime_type=dam_asset.mime_type,
                extension=dam_asset.extension,
                brand_id=dam_asset.brand_id,
                tags=dam_asset.tags,
                url=dam_asset.url,
                state=dam_asset.state,
                description=dam_asset.description,
                temporary=dam_asset.temporary,
                meta_info=dam_asset.meta_info,
            ))
        if assets_dir:
            shutil.rmtree(assets_dir, ignore_errors=True)
        return PutAssetsResult(
            dam_assets=dam_assets,
            dam_asset_batch=DamAssetBatchDTO(
                uuid=batch.uuid,
                resource_type=batch.resource_type,
                initiator=batch.initiator,
                description=batch.description,
            )
        )
