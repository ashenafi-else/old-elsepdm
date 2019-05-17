import os
import shutil
from unittest.mock import Mock

from django.conf import settings
from elsedam.models import (
    DamAsset,
    BufferedDamAsset,
)
from elsedam.tests.test_base_dam import TestBaseDam
from elsecommon.transports.router import Router
from elsecommon.transports.transportabc import TransportABC
from elsecommon.transports.operation_type import OperationType
from elsepublic.elsedam.buffering_assets.dto import (
    PutAssetsToBufferParams,
    PutAssetsToBufferResult,
)
from elsepublic.elsedam.interfaces.put_assets_to_buffer_operation import (
    PutAssetsToBufferOpInterface,
)


class TestPutAssetsToBufferOperation(TestBaseDam):
    test_path = os.path.dirname(os.path.realpath(__file__))
    fixtures_path = os.path.join(test_path, 'fixtures')
    fixtures_models_path = os.path.join(
        test_path, 'fixtures', 'common_test_data.json')
    dam_assets_models_path = os.path.join(
        test_path, 'fixtures', 'dam_assets_data.json')
    fixtures = (fixtures_models_path, dam_assets_models_path,)

    def setUp(self):
        super().setUp()
        dam_asset_uuids = DamAsset.objects.values_list('uuid', flat=True)
        self.put_assets_to_buffer_dto = PutAssetsToBufferParams(
            dam_asset_uuids=dam_asset_uuids)
        Router[PutAssetsToBufferOpInterface] = OperationType(
            expose=False, producer=TransportABC)
        self.mock_object.put_by_url = Mock(return_value=True)
        input_file = os.path.join(self.fixtures_path, 'test.png')
        settings.BUFFER_SERVICE.open_buffer_file = Mock(
            return_value=open(input_file, 'rb'))
        settings.BUFFER_SERVICE.copy_to_temp = Mock(return_value=input_file)
        shutil.rmtree = Mock(return_value=None)

    def test_put_assets_to_buffer(self):
        """
        Test put and remove assets from buffer operations
        """
        put_op = Router[PutAssetsToBufferOpInterface.uri]
        put_result = put_op(self.put_assets_to_buffer_dto)
        self.assertIsInstance(put_result, PutAssetsToBufferResult)
        self.assertEqual(len(put_result.dam_asset_requests),
                         len(self.put_assets_to_buffer_dto.dam_asset_uuids))
        put_states = [
            request.buffered_asset.state for request in put_result.dam_asset_requests]
        self.assertNotIn(BufferedDamAsset.FAILED_STATE, put_states)
