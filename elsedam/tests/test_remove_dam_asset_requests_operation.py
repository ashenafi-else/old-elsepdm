import os
from elsecommon.transports.router import Router
from elsecommon.transports.operation_type import OperationType
from elsecommon.transports.transportabc import TransportABC
from elsedam.models import (
    DamAssetRequest,
    BufferedDamAsset,
)
from elsedam.tests.test_base_dam import TestBaseDam
from elsepublic.elsedam.dto.remove_dam_asset_requests_operation import (
    RemoveDamAssetRequestsParameters,
    RemoveDamAssetRequestsResult,
)
from elsepublic.elsedam.interfaces.remove_dam_asset_requests_operation import RemoveDamAssetRequestsOpInterface


class TestRemoveDamAssetRequestsOperation(TestBaseDam):
    test_path = os.path.dirname(os.path.realpath(__file__))
    fixtures_path = os.path.join(test_path, 'fixtures')
    fixtures_models_path = os.path.join(test_path, 'fixtures', 'common_test_data.json')
    dam_assets_models_path = os.path.join(test_path, 'fixtures', 'dam_assets_data.json')
    buffered_dam_assets_models_path = os.path.join(test_path, 'fixtures', 'buffered_dam_assets_data.json')
    dam_asset_requests_models_path = os.path.join(test_path, 'fixtures', 'dam_asset_requests_data.json')
    fixtures = (
        fixtures_models_path, dam_assets_models_path, buffered_dam_assets_models_path, dam_asset_requests_models_path,)

    def setUp(self):
        super().setUp()
        dam_asset_requests = DamAssetRequest.objects.values_list('uuid', flat=True)
        self.remove_dam_asset_requests_dto = RemoveDamAssetRequestsParameters(dam_asset_requests=dam_asset_requests)
        Router[RemoveDamAssetRequestsOpInterface] = OperationType(expose=False, producer=TransportABC)

    def test_remove_dam_asset_requests(self):
        """
        Test put and remove assets from buffer operations
        """
        rem_req_op = Router[RemoveDamAssetRequestsOpInterface.uri]
        rem_req_result = rem_req_op(self.remove_dam_asset_requests_dto)
        self.assertIsInstance(rem_req_result, RemoveDamAssetRequestsResult)
        self.assertTrue(rem_req_result)
        self.assertEqual(DamAssetRequest.objects.all().count(), 0)
        all_buf_assets = BufferedDamAsset.objects.all()
        for_remove_buf_assets = all_buf_assets.filter(for_removing=True)
        self.assertEqual(all_buf_assets.count(), for_remove_buf_assets.count())
