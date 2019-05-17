import os
from unittest.mock import Mock
from elsecommon.transports.operation_type import OperationType
from elsecommon.transports.transportabc import TransportABC
from elsecommon.transports.router import Router
from elsedam.models import BufferedDamAsset
from elsedam.tests.test_base_dam import TestBaseDam
from elsepublic.elsedam.dto.remove_assets_from_buffer_operation import (
    RemoveAssetsFromBufferParameters,
    RemoveAssetsFromBufferResult,
)
from elsepublic.elsedam.interfaces.remove_assets_from_buffer_operation import RemoveAssetsFromBufferOpInterface


class TestRemoveAssetsFromBufferOperation(TestBaseDam):
    test_path = os.path.dirname(os.path.realpath(__file__))
    fixtures_path = os.path.join(test_path, 'fixtures')
    fixtures_models_path = os.path.join(test_path, 'fixtures', 'common_test_data.json')
    dam_assets_models_path = os.path.join(test_path, 'fixtures', 'dam_assets_data.json')
    buffered_dam_assets_models_path = os.path.join(test_path, 'fixtures', 'buffered_dam_assets_data.json')
    fixtures = (fixtures_models_path, dam_assets_models_path, buffered_dam_assets_models_path,)

    def setUp(self):
        super().setUp()
        Router[RemoveAssetsFromBufferOpInterface] = OperationType(expose=False, producer=TransportABC)
        self.mock_object.remove = Mock(return_value=True)

    def test_remove_assets_from_buffer(self):
        """
        Test remove assets from buffer operation
        """
        rem_assets_op = Router[RemoveAssetsFromBufferOpInterface.uri]
        rem_assets_result = rem_assets_op(RemoveAssetsFromBufferParameters())
        self.assertIsInstance(rem_assets_result, RemoveAssetsFromBufferResult)
        self.assertTrue(rem_assets_result.success)
        self.assertEqual(len(rem_assets_result.failed_uuids), 0)
        states = BufferedDamAsset._base_manager.values_list('state', flat=True)
        self.assertNotIn(BufferedDamAsset.FAILED_REMOVE_STATE, states)
        self.assertEqual(BufferedDamAsset.objects.all().count(), 0)
