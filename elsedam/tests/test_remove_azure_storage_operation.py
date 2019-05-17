from elsecommon.transports.router import Router
from elsecommon.transports.operation_type import OperationType
from elsecommon.transports.transportabc import TransportABC
from elsedam.models import AzureStorage
from elsedam.tests.test_base_dam import TestBaseDam
from elsepublic.elsedam.dto.remove_azure_storage_operation import (
    RemoveAzureStorageParameters,
    RemoveAzureStorageResult,
)
from elsepublic.elsedam.interfaces.remove_azure_storage_operation import RemoveAzureStorageOpInterface


class TestRemoveAzureStorageOperation(TestBaseDam):
    def setUp(self):
        super().setUp()
        self.public_azure_storage = AzureStorage.objects.filter(uuid='642bbbe6-d21b-11e8-a8d5-f2801f1b9fd2').first()
        self.remove_azure_storage_dto = RemoveAzureStorageParameters(uuid=self.public_azure_storage.uuid)
        self.remove_not_existed_azure_storage_dto = RemoveAzureStorageParameters(
            uuid='322bbbe6-d21b-11e8-a8d5-f2801f1b9fd2')
        Router[RemoveAzureStorageOpInterface] = OperationType(expose=False, producer=TransportABC)

    def test_remove_azure_storage(self):
        """
        Test remove azure storage
        """
        rem_op = Router[RemoveAzureStorageOpInterface.uri]
        remove_result = rem_op(self.remove_azure_storage_dto)
        self.assertIsInstance(remove_result, RemoveAzureStorageResult)
        self.assertTrue(remove_result.success)
        self.assertIsNone(AzureStorage.objects.filter(uuid=self.public_azure_storage.uuid).first())

    def test_remove_not_existed_azure_storage(self):
        """
        Test remove not existed azure storage
        """
        rem_op = Router[RemoveAzureStorageOpInterface.uri]
        remove_result = rem_op(self.remove_not_existed_azure_storage_dto)
        self.assertIsInstance(remove_result, RemoveAzureStorageResult)
        self.assertFalse(remove_result.success)
