from elsepdm.tests.test_base_pdm import TestBasePdm
from elsepdm.operations.add_product_structure_assets import AddProductStructureAssetsOperation
from elsepublic.elsedam.asset_extensions import AssetExtensions
from elsepublic.elsedam.resource_types import ResourceTypes
from elsepublic.elsepdm.dto.add_product_structure_assets import AddProductStructureAssetsParamsDTO
from elsepublic.dto.dam_asset_info import DamAssetInfoDTO
from elsepdm.models import (
    Product,
    ProductRevision,
    ProductComponent,
    ProductStructure,
    ComponentAsset,
)
from elsepublic.exceptions import MissingProductStructureException


class TestAddProductStructureAssetsOperation(TestBasePdm):
    def setUp(self):
        super().setUp()

        test_product = Product.objects.create(
            collection=self.collection,
            name="test_product",
            sku="test_pr",
            product_hierarchy=self.root,
            description="It's a test product",
        )

        test_revision = ProductRevision.objects.create(product=test_product)
        test_component = ProductComponent.objects.create(
            product=test_revision,
            name='test_name',
            component='test_comp',
            order=1,
        )
        self.test_structure = ProductStructure.objects.create(
            component=test_component,
            name='test_structure',
            export_name='test_str',
            structure='test-str',
        )
        self.test_asset = DamAssetInfoDTO(
            dam_uuid=self.fake_uuid,
            filename='test_file',
            size='1',
            extension=AssetExtensions.OBJ,
            brand_id=self.fake_uuid,
            url='google.com',
            state='test_state',
            resource_type=ResourceTypes.COMPONENT_OBJ,
            meta_info='',
        )
        structures_mapping = {str(self.test_structure.uuid): self.test_asset}
        self.add_product_structure_assets_dto = AddProductStructureAssetsParamsDTO(
            structures_mapping=structures_mapping,
        )
        self.add_missing_product_structure_assets_dto = AddProductStructureAssetsParamsDTO(
            structures_mapping={self.fake_uuid: self.test_asset},
        )
        self.add_product_structure_assets_op = AddProductStructureAssetsOperation()

    def test_add_product_structure_assets(self):
        """
        Test add product structure assets
        """
        result = self.add_product_structure_assets_op(self.add_product_structure_assets_dto)

        self.assertIsNone(result)
        created_asset = self.test_structure.assets.first()

        self.assertEqual(self.test_asset.dam_uuid, str(created_asset.dam_uuid))
        self.assertEqual(self.test_asset.filename, created_asset.filename)
        self.assertEqual(self.test_asset.size, str(created_asset.size))
        self.assertEqual(self.test_asset.extension, created_asset.extension)
        self.assertEqual(self.test_asset.brand_id, str(created_asset.brand_id))
        self.assertEqual(self.test_asset.url, created_asset.url)
        self.assertEqual(self.test_asset.state, created_asset.state)
        self.assertEqual(self.test_asset.meta_info, created_asset.meta_info)
        self.assertEqual(self.test_asset.resource_type, created_asset.resource_type)
        self.assertEqual(ComponentAsset.OBJ_ASSET, created_asset.asset_type)

    def test_import_missing_structure_from_obj(self):
        """
        Test import missing structure from obj
        """
        with self.assertRaises(MissingProductStructureException):
            self.add_product_structure_assets_op(self.add_missing_product_structure_assets_dto)

