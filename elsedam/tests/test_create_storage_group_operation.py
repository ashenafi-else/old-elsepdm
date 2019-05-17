from elsecommon.transports.operation_type import OperationType
from elsecommon.transports.transportabc import TransportABC
from elsecommon.transports.router import Router

from elsedam.tests.test_base_dam import TestBaseDam
from elsepublic.elsedam.dto.create_storage_group_operation import (
    CreateStorageGroupParameters,
    CreateStorageGroupResult,
)
from elsepublic.elsedam.interfaces.create_storage_group_operation import CreateStorageGroupOpInterface


class TestCreateStorageGroupOperation(TestBaseDam):
    def setUp(self):
        super().setUp()
        self.create_storage_group_dto = CreateStorageGroupParameters(
            file_extensions=["json", "png", "jpg"],
            mime_types=["application/json"],
            name="test_storage_group",
            storage_uuid='642bbbe6-d21b-11e8-a8d5-f2801f1b9fd2',
            path='testpath',
            tags=["a", "c", "b"],
        )
        self.create_existed_storage_group_dto = CreateStorageGroupParameters(
            file_extensions=["json", "png", "jpg"],
            mime_types=["application/json"],
            name="publicgroup",
            storage_uuid='642bbbe6-d21b-11e8-a8d5-f2801f1b9fd3',
            path='public_azure_location',
            tags=["a", "c", "b"],
        )
        Router[CreateStorageGroupOpInterface] = OperationType(expose=False, producer=TransportABC)

    def test_create_storage_group(self):
        """
        Test create storage group
        """
        cre_op = Router[CreateStorageGroupOpInterface.uri]
        create_result = cre_op(self.create_storage_group_dto)
        self.assertIsInstance(create_result, CreateStorageGroupResult)
        self.assertEqual(create_result.file_extensions, self.create_storage_group_dto.file_extensions)
        self.assertEqual(create_result.mime_types, self.create_storage_group_dto.mime_types)
        self.assertEqual(create_result.name, self.create_storage_group_dto.name)
        self.assertEqual(create_result.tags, self.create_storage_group_dto.tags)

    def test_create_existed_storage_group(self):
        """
        Test create existed storage group
        """
        cre_op = Router[CreateStorageGroupOpInterface.uri]
        with self.assertRaises(RuntimeError):
            cre_op(self.create_existed_storage_group_dto)
