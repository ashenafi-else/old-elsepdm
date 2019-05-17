import os
from unittest.mock import Mock
from elsecommon.transports.operation_type import OperationType
from elsecommon.transports.transportabc import TransportABC
from elsecommon.transports.router import Router
from elsedam.models import (
    StorageGroup,
    DamAsset,
)
from elsedam.tests.test_base_dam import TestBaseDam
from elsepublic.elsedam.dto.remove_storage_group_operation import (
    RemoveStorageGroupParameters,
    RemoveStorageGroupResult,
)
from elsepublic.elsedam.interfaces.remove_storage_group_operation import RemoveStorageGroupOpInterface


class TestRemoveStorageGroupOperation(TestBaseDam):
    test_path = os.path.dirname(os.path.realpath(__file__))
    fixtures_path = os.path.join(test_path, 'fixtures')
    fixtures_models_path = os.path.join(test_path, 'fixtures', 'common_test_data.json')
    dam_assets_models_path = os.path.join(test_path, 'fixtures', 'private_dam_assets_data.json')
    fixtures = (fixtures_models_path, dam_assets_models_path)

    def setUp(self):
        super().setUp()
        self.azure_private_group = StorageGroup.objects.filter(uuid='642bbbe6-d21b-11e8-a8d5-f2801f1b9fa1').first()
        self.remove_storage_group_dto = RemoveStorageGroupParameters(uuid=self.azure_private_group.uuid)
        self.remove_not_existed_storage_group_dto = RemoveStorageGroupParameters(
            uuid='112bbbe6-d21b-11e8-a8d5-f2801f1b9fa1')
        Router[RemoveStorageGroupOpInterface] = OperationType(expose=False, producer=TransportABC)
        self.mock_object.remove = Mock(return_value=True)

    def test_remove_storage_group(self):
        """
        Test remove storage group
        """
        rem_op = Router[RemoveStorageGroupOpInterface.uri]
        remove_result = rem_op(self.remove_storage_group_dto)
        self.assertIsInstance(remove_result, RemoveStorageGroupResult)
        self.assertTrue(remove_result.success)
        self.assertIsNone(StorageGroup.objects.filter(uuid=self.azure_private_group.uuid).first())
        self.assertEqual(DamAsset.objects.filter(group__uuid=self.azure_private_group.uuid).count(), 0)

    def test_remove_not_existed_storage_group(self):
        """
        Test remove not existed storage group
        """
        rem_op = Router[RemoveStorageGroupOpInterface.uri]
        remove_result = rem_op(self.remove_not_existed_storage_group_dto)
        self.assertIsInstance(remove_result, RemoveStorageGroupResult)
        self.assertFalse(remove_result.success)
