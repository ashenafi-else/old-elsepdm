from elsepdm.models import (
    Product,
    ComponentAsset,
    ProductRevision,
    ProductComponent,
    ProductStructure,
)
from elsepdm.tests.test_base_pdm import TestBasePdm
from elsepublic.elsedam.put_assets.dto import (
    PutAssetResult,
    PutAssetsResult,
    DamAssetBatchDTO,
)
from elsepublic.elsedam.resource_types import ResourceTypes
from elsepdm.operations.import_from_obj.import_structure_from_obj_handler import (
    ImportStructureFromObjSuccessHandler, )


class TestImportStructureFromObjSuccessHandler(TestBasePdm):
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
        self.import_structure_from_obj_handler_dto = PutAssetsResult(
            dam_assets=[PutAssetResult(
                uuid=self.fake_uuid,
                filename='test_asset',
                size='1',
                mime_type='test_type',
                extension='.blend',
                brand_id=self.fake_uuid,
                tags=[],
                url='google.com',
                state='test_state',
                description='test description',
                temporary=False,
                meta_info='',
            )],
            dam_asset_batch=DamAssetBatchDTO(
                uuid=self.fake_uuid,
                resource_type=ResourceTypes.BLENDER_MODEL,
                initiator='test_init',
                description='test description',
            ),
        )
        self.context = {'structure_uuid': self.test_structure.uuid}

        self.import_structure_from_obj_success_handler = ImportStructureFromObjSuccessHandler()

    def test_import_structure_from_obj_handler(self):
        """
        Test import structure from obj handler
        """
        result = self.import_structure_from_obj_success_handler(
            self.import_structure_from_obj_handler_dto,
            **self.context,
        )
        self.assertIsNone(result)
        created_asset = self.test_structure.assets.first()

        dam_asset_info = self.import_structure_from_obj_handler_dto.dam_assets[0]
        self.assertEqual(dam_asset_info.uuid, str(created_asset.dam_uuid))
        self.assertEqual(dam_asset_info.filename, created_asset.filename)
        self.assertEqual(dam_asset_info.size, str(created_asset.size))
        self.assertEqual(dam_asset_info.extension, created_asset.extension)
        self.assertEqual(dam_asset_info.brand_id, str(created_asset.brand_id))
        self.assertEqual(dam_asset_info.url, created_asset.url)
        self.assertEqual(dam_asset_info.state, created_asset.state)
        self.assertEqual(dam_asset_info.meta_info, created_asset.meta_info)
        self.assertEqual(ComponentAsset.MODEL_ASSET, created_asset.asset_type)
        self.assertEqual(
            self.import_structure_from_obj_handler_dto.dam_asset_batch.resource_type,
            created_asset.resource_type,
        )
