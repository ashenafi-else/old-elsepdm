import os
import shutil
from unittest.mock import Mock

from django.conf import settings
from elsedam.models import DamAsset
from django.core.files import File
from elsedam.tests.test_base_dam import TestBaseDam
from elsepublic.elsedam.put_assets.dto import (
    PutAssetsParams,
    PutAssetsResult,
    PutAssetParameters,
)
from elsedam.operations.put_assets.put_assets import PutAssetsOperation


class TestPutAssetsOperation(TestBaseDam):
    def setUp(self):
        super().setUp()
        put_assets_dto = []
        input_file = os.path.join(self.fixtures_path, 'test.png')
        for i in range(3):
            stream = open(input_file, 'rb')
            file = File(stream)
            put_asset_dto = PutAssetParameters(
                filename=os.path.basename(file.name),
                brand_id=self.brand.brand_external_id,
                tags=['x', 'y', 'z'],
                file=stream,
                temporary=False,
            )
            put_assets_dto.append(put_asset_dto)
        put_assets_dto[0].tags = ['a', 'b', 'c']
        put_assets_dto[1].brand_id = self.default_brand.brand_external_id
        put_assets_dto[2].relative_path = 'test_folder'

        self.op = PutAssetsOperation()
        self.put_assets_dto = PutAssetsParams(
            base_assets=put_assets_dto,
            resource_type='type',
            initiator='initiator',
        )
        self.mock_object.put_by_stream = Mock(return_value=True)
        settings.BUFFER_SERVICE.open_buffer_file = Mock(
            return_value=open(input_file, 'rb'))
        shutil.rmtree = Mock(return_value=None)

    def test_put_assets_operations(self):
        """
        Test put assets operations
        """
        put_result = self.op(self.put_assets_dto)
        self.assertIsInstance(put_result, PutAssetsResult)
        self.assertTrue(hasattr(put_result, 'dam_assets'))
        self.assertEqual(len(put_result.dam_assets),
                         len(self.put_assets_dto.base_assets))
        put_dam_assets_states = [
            dam_asset.state for dam_asset in put_result.dam_assets]
        self.assertEqual(
            self.put_assets_dto.resource_type,
            put_result.dam_asset_batch.resource_type)
        self.assertEqual(
            self.put_assets_dto.initiator,
            put_result.dam_asset_batch.initiator)
        self.assertEqual(
            self.put_assets_dto.description,
            put_result.dam_asset_batch.description)
        self.assertNotIn(DamAsset.FAILED_STATE, put_dam_assets_states)
