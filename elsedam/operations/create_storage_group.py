import logging
from elsecommon import marshalling
from elsedam.models import StorageGroup, StorageLocation, Storage
from elsepublic.elsedam.dto.create_storage_group_operation import (
    CreateStorageGroupParameters,
    CreateStorageGroupResult,
)
from elsepublic.elsedam.exceptions.storage_group_exceptions import ExistedStorageGroupException
from elsepublic.elsedam.serializers.create_storage_group_operation import (
    CreateStorageGroupSerializer,
    CreateStorageGroupResultSerializer,
)

logger = logging.getLogger()


class CreateStorageGroupOperation(marshalling.ElseOperation):
    """
    Operation for storage group creation.

    Attributes
    ----------
    expect_serializer_class : elseserializers.BaseDtoSerializer
        Expect serializer.
    expose_serializer_class : elseserializers.BaseDtoSerializer
        Expose serializer.
    """
    expect_serializer_class = CreateStorageGroupSerializer
    expose_serializer_class = CreateStorageGroupResultSerializer

    def __call__(self, data: CreateStorageGroupParameters, **context) -> CreateStorageGroupResult:
        storage = Storage.objects.filter(uuid=data.storage_uuid).first()
        storage_group = StorageGroup.objects.filter(
            brand=storage.brand,
            file_extensions=data.file_extensions,
            mime_types=data.mime_types,
            name=data.name,
            tags=data.tags,
            location__path=data.path,
        )
        if storage_group:
            raise ExistedStorageGroupException
        location, created = StorageLocation.objects.get_or_create(storage=storage, path=data.path)
        storage_group = StorageGroup.objects.create(
            brand=location.storage.brand,
            file_extensions=data.file_extensions,
            mime_types=data.mime_types,
            name=data.name,
            tags=data.tags,
            location=location,
        )
        return CreateStorageGroupResult(
            uuid=storage_group.uuid,
            file_extensions=storage_group.file_extensions,
            mime_types=storage_group.mime_types,
            tags=storage_group.tags,
            name=storage_group.name,
            location_uuid=storage_group.location.uuid,
            brand_uuid=storage_group.brand.uuid,
            created=storage_group.created,
            updated=storage_group.updated,
        )
