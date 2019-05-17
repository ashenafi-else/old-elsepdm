import logging

from elsecommon import marshalling
from elsecommon.transports.router import Router
from elsedam.models import StorageGroup, Storage
from elsepublic.elsedam.dto.remove_assets_operation import RemoveAssetsParameters
from elsepublic.elsedam.dto.remove_storage_group_operation import (
    RemoveStorageGroupParameters,
    RemoveStorageGroupResult,
)
from elsepublic.elsedam.interfaces.remove_assets_operation import RemoveAssetsOpInterface
from elsepublic.elsedam.serializers.remove_storage_group_operation import (
    RemoveStorageGroupSerializer,
    RemoveStorageGroupResultSerializer,
)

logger = logging.getLogger()


class RemoveStorageGroupOperation(marshalling.ElseOperation):
    """
    Operation for storage group removing.

    Attributes
    ----------
    expect_serializer_class : elseserializers.BaseDtoSerializer
        Expect serializer.
    expose_serializer_class : elseserializers.BaseDtoSerializer
        Expose serializer.
    """
    expect_serializer_class = RemoveStorageGroupSerializer
    expose_serializer_class = RemoveStorageGroupResultSerializer

    def __call__(self, data: RemoveStorageGroupParameters, **context) -> RemoveStorageGroupResult:
        storage_group = StorageGroup.objects.filter(uuid=data.uuid).first()
        if storage_group:
            if storage_group.location.storage.storage_type == Storage.TYPE_PRIVATE:
                dam_assets_uuids = storage_group.assets.values_list('uuid', flat=True)
                remove_assets = Router[RemoveAssetsOpInterface.uri]
                remove_assets(RemoveAssetsParameters(dam_assets_uuids=dam_assets_uuids, **context))
            storage_group.delete()
            return RemoveStorageGroupResult(success=True)
        return RemoveStorageGroupResult(success=False)
