from elsecommon.transports.router import Router
from elsecommon.transports.operation_type import OperationType
from elsecommon.transports.transportabc import TransportABC
from elsedam.models import AzureStorage
from elsedam.tests.test_base_dam import TestBaseDam
from elsepublic.elsedam.dto.create_azure_storage_operation import (
    CreateAzureStorageParameters,
    CreateAzureStorageResult,
)
from elsepublic.elsedam.interfaces.create_azure_storage_operation import CreateAzureStorageOpInterface


class TestCreateAzureStorageOperation(TestBaseDam):
    def setUp(self):
        super().setUp()
        self.create_azure_storage_dto = CreateAzureStorageParameters(
            brand_uuid=self.brand.uuid,
            domain='testdomain',
            container='container',
            account_name='testazureaccount',
            account_key='testazurekey',
            storage_type=AzureStorage.TYPE_PUBLIC,
            storage_timeout=60,
            is_default=False,
        )
        self.create_existed_azure_storage_dto = CreateAzureStorageParameters(
            brand_uuid=self.brand.uuid,
            domain='testdomain',
            container='public',
            account_name='elsedamstorage',
            account_key='testazurekey',
            storage_type=AzureStorage.TYPE_PUBLIC,
            storage_timeout=60,
            is_default=False,
        )
        Router[CreateAzureStorageOpInterface] = OperationType(expose=False, producer=TransportABC)

    def test_create_azure_storage(self):
        """
        Test remove azure storage
        """
        cre_op = Router[CreateAzureStorageOpInterface.uri]
        create_result = cre_op(self.create_azure_storage_dto)
        self.assertIsInstance(create_result, CreateAzureStorageResult)
        self.assertEqual(create_result.brand_uuid, self.create_azure_storage_dto.brand_uuid)
        self.assertEqual(create_result.domain, self.create_azure_storage_dto.domain)
        self.assertEqual(create_result.account_name, self.create_azure_storage_dto.account_name)
        self.assertEqual(create_result.account_key, self.create_azure_storage_dto.account_key)
        self.assertEqual(create_result.storage_type, self.create_azure_storage_dto.storage_type)
        self.assertEqual(create_result.storage_timeout, self.create_azure_storage_dto.storage_timeout)
        self.assertFalse(create_result.is_default)
        self.assertEqual(create_result.model_type, 'azurestorage')

    def test_create_existed_azure_storage(self):
        cre_op = Router[CreateAzureStorageOpInterface.uri]
        with self.assertRaises(RuntimeError):
            cre_op(self.create_existed_azure_storage_dto)
