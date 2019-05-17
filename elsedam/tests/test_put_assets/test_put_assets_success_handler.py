from django.test import TestCase
from elsepublic.dto.dam_asset_info import DamAssetsInfoDTO
from elsepublic.elsedam.put_assets.dto import (
    PutAssetResult,
    PutAssetsResult,
)
from elsedam.operations.put_assets.put_assets_success_handler import (
    PutAssetsSuccessHandler,
)


class TestPutAssetsSuccessHandler(TestCase):
    def setUp(self):
        self.put_assets_handler_dto = PutAssetsResult(dam_assets=[
            PutAssetResult(
                uuid='62f49d28-f5b5-4b05-ab60-21fa7afff4c2',
                filename='filename',
                size=1234,
                mime_type='mime_type',
                extension='.png',
                brand_id='0',
                tags=['x'],
                url='https://url.com',
                state='state',
                resource_type='resource_type',
                description='description',
                temporary=False,
                meta_info='',
            )]
        )

        self.op = PutAssetsSuccessHandler()

    def test_put_assets_success_handler(self):
        """
        Test put assets success handler
        """
        handler_result = self.op(self.put_assets_handler_dto)
        self.assertIsInstance(handler_result, DamAssetsInfoDTO)
        self.assertEqual(len(handler_result.dam_assets_info),
                         len(self.put_assets_handler_dto.dam_assets))
        dam_asset_info = handler_result.dam_assets_info[0]
        self.assertEqual(dam_asset_info.dam_uuid,
                         self.put_assets_handler_dto.dam_assets[0].uuid)
        self.assertEqual(dam_asset_info.filename,
                         self.put_assets_handler_dto.dam_assets[0].filename)
        self.assertEqual(
            dam_asset_info.size,
            self.put_assets_handler_dto.dam_assets[0].size)
        self.assertEqual(dam_asset_info.extension,
                         self.put_assets_handler_dto.dam_assets[0].extension)
        self.assertEqual(dam_asset_info.brand_id,
                         self.put_assets_handler_dto.dam_assets[0].brand_id)
        self.assertEqual(
            dam_asset_info.url,
            self.put_assets_handler_dto.dam_assets[0].url)
        self.assertEqual(dam_asset_info.state,
                         self.put_assets_handler_dto.dam_assets[0].state)
        self.assertEqual(dam_asset_info.meta_info,
                         self.put_assets_handler_dto.dam_assets[0].meta_info)
