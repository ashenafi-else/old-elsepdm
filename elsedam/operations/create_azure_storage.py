import logging
from elsecommon import marshalling
from elsedam.models import Brand, AzureStorage
from elsepublic.elsedam.dto.create_azure_storage_operation import (
    CreateAzureStorageParameters,
    CreateAzureStorageResult,
)
from elsepublic.elsedam.exceptions.azure_storage_exceptions import ExistedAzureStorageException
from elsepublic.elsedam.serializers.create_azure_storage_operation import (
    CreateAzureStorageSerializer,
    CreateAzureStorageResultSerializer,
)

logger = logging.getLogger()


class CreateAzureStorageOperation(marshalling.ElseOperation):
    """
    Operation for azure storage creation.

    Attributes
    ----------
    expect_serializer_class : elseserializers.BaseDtoSerializer
        Expect serializer.
    expose_serializer_class : elseserializers.BaseDtoSerializer
        Expose serializer.
    """
    expect_serializer_class = CreateAzureStorageSerializer
    expose_serializer_class = CreateAzureStorageResultSerializer

    def __call__(self, data: CreateAzureStorageParameters, **context) -> CreateAzureStorageResult:
        brand = Brand.objects.filter(uuid=data.brand_uuid).first()
        storage = AzureStorage.objects.filter(
            brand=brand,
            account_name=data.account_name,
            container=data.container,
        ).first()
        if storage:
            raise ExistedAzureStorageException
        storage = AzureStorage.objects.create(
            brand=brand,
            domain=data.domain,
            account_name=data.account_name,
            container=data.container,
            account_key=data.account_key,
            storage_type=data.storage_type,
            storage_timeout=data.storage_timeout,
        )
        return CreateAzureStorageResult(
            uuid=storage.uuid,
            brand_uuid=storage.brand.uuid,
            domain=storage.domain,
            storage_type=storage.storage_type,
            is_default=storage.is_default,
            account_name=storage.account_name,
            account_key=storage.account_key,
            container=storage.container,
            storage_timeout=storage.storage_timeout,
            model_type=storage.model_type,
        )
