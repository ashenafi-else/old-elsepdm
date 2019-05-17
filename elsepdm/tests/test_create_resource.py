from elsepdm.models import ResourceAsset
from elsepublic.exceptions import (
    MissingBrandException,
    InvalidResourceTypeException,
)
from elsepdm.tests.test_base_pdm import TestBasePdm
from elsepublic.dto.dam_asset_info import DamAssetInfoDTO
from elsepublic.elsedam.resource_types import ResourceTypes
from elsepdm.operations.create_resource import CreateResourceOperation
from elsepublic.elsepdm.create_resource import (
    CreateResourceParams,
    CreateResourceResult,
)
from elsepublic.elsedam.asset_extensions import AssetExtensions


class TestCreateResourceOperation(TestBasePdm):
    def setUp(self):
        super().setUp()
        self.DAM_asset_info = DamAssetInfoDTO(
            dam_uuid=self.fake_uuid,
            filename='name',
            size=256,
            extension=AssetExtensions.PNG,
            brand_id='1',
            url='www.google.com',
            state='state',
            resource_type=ResourceTypes.BLENDER_RESOURCE,
            meta_info='',
        )
        self.dto = CreateResourceParams(
            dam_asset_info=self.DAM_asset_info,
            brand_uuid=self.brand.uuid,
            resource_type=ResourceAsset.TYPE_BACKGROUND,
            name='Test name',
        )
        self.dto_with_wrong_brand = CreateResourceParams(
            dam_asset_info=self.DAM_asset_info,
            brand_uuid=self.fake_uuid,
            resource_type=ResourceAsset.TYPE_BACKGROUND,
            name='Test name',
        )

        self.dto_with_invalid_asset_type = CreateResourceParams(
            dam_asset_info=self.DAM_asset_info,
            brand_uuid=self.brand.uuid,
            resource_type='Not a valid resource type',
            name='Test name',
        )

        self.op = CreateResourceOperation()

    def test_create_resource(self):
        """
        Test create resource
        """
        result = self.op(data=self.dto)
        self.assertIsInstance(result, CreateResourceResult)
        resource = ResourceAsset.objects.get(uuid=result.resource_uuid)

        self.assertEqual(resource.type, self.dto.resource_type)
        self.assertEqual(resource.name, self.dto.name)
        self.assertEqual(resource.pdm_brand.uuid, self.dto.brand_uuid)
        self.assertEqual(resource.asset_type, ResourceAsset.RESOURCE_ASSET)
        self.assertEqual(str(resource.dam_uuid), self.DAM_asset_info.dam_uuid)
        self.assertEqual(resource.filename, self.DAM_asset_info.filename)
        self.assertEqual(str(resource.size), self.DAM_asset_info.size)
        self.assertEqual(resource.extension, self.DAM_asset_info.extension)
        self.assertEqual(resource.brand_id, self.DAM_asset_info.brand_id)
        self.assertEqual(resource.url, self.DAM_asset_info.url)
        self.assertEqual(resource.state, self.DAM_asset_info.state)
        self.assertEqual(
            resource.resource_type,
            self.DAM_asset_info.resource_type)
        self.assertEqual(resource.meta_info, self.DAM_asset_info.meta_info)

    def test_create_resource_with_wrong_brand(self):
        """
        Test create resource with wrong brand
        """
        with self.assertRaises(MissingBrandException):
            self.op(data=self.dto_with_wrong_brand)

    def test_create_resource_with_wrong_asset_type(self):
        """
        Test create resource with wrong asset type
        """
        with self.assertRaises(InvalidResourceTypeException):
            self.op(self.dto_with_invalid_asset_type)
