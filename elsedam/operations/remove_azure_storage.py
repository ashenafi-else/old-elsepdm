import logging

from elsecommon import marshalling
from elsedam.models import AzureStorage
from elsepublic.elsedam.dto.remove_azure_storage_operation import (
    RemoveAzureStorageParameters,
    RemoveAzureStorageResult,
)
from elsepublic.elsedam.serializers.remove_azure_storage_operation import (
    RemoveAzureStorageSerializer,
    RemoveAzureStorageResultSerializer,
)

logger = logging.getLogger()


class RemoveAzureStorageOperation(marshalling.ElseOperation):
    """
    Operation for azure storage removing.

    Attributes
    ----------
    expect_serializer_class : elseserializers.BaseDtoSerializer
        Expect serializer.
    expose_serializer_class : elseserializers.BaseDtoSerializer
        Expose serializer.
    """
    expect_serializer_class = RemoveAzureStorageSerializer
    expose_serializer_class = RemoveAzureStorageResultSerializer

    def __call__(self, data: RemoveAzureStorageParameters, **context) -> RemoveAzureStorageResult:
        storage = AzureStorage.objects.filter(uuid=data.uuid).first()
        if storage:
            storage.delete()
            return RemoveAzureStorageResult(success=True)
        return RemoveAzureStorageResult(success=False)
