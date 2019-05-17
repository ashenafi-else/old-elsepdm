import os
from unittest.mock import Mock
from elsecommon.transports.operation_type import OperationType
from elsecommon.transports.router import Router
from elsecommon.transports.transportabc import TransportABC
from elsedam.models import DamAsset
from elsedam.tests.test_base_dam import TestBaseDam
from elsepublic.elsedam.dto.remove_assets_operation import (
    RemoveAssetsParameters,
    RemoveAssetsResult,
)
from elsepublic.elsedam.interfaces.remove_assets_operation import RemoveAssetsOpInterface


class TestRemoveAssetsOperation(TestBaseDam):
    test_path = os.path.dirname(os.path.realpath(__file__))
    fixtures_path = os.path.join(test_path, 'fixtures')
    fixtures_models_path = os.path.join(test_path, 'fixtures', 'common_test_data.json')
    dam_assets_models_path = os.path.join(test_path, 'fixtures', 'dam_assets_data.json')
    fixtures = (fixtures_models_path, dam_assets_models_path,)

    def setUp(self):
        super().setUp()
        dam_assets_uuids = DamAsset.objects.values_list('uuid', flat=True)
        self.remove_assets_dto = RemoveAssetsParameters(dam_assets_uuids=dam_assets_uuids)
        Router[RemoveAssetsOpInterface] = OperationType(expose=False, producer=TransportABC)
        self.mock_object.remove = Mock(return_value=True)

    def test_remove_assets_operations(self):
        """
        Test remove assets operations
        """
        rem_op = Router[RemoveAssetsOpInterface.uri]
        rem_result = rem_op(self.remove_assets_dto)
        self.assertIsInstance(rem_result, RemoveAssetsResult)
        self.assertTrue(rem_result.success)
        self.assertEqual(len(rem_result.failed_uuids), 0)
        self.assertEqual(DamAsset.objects.all().count(), 0)
