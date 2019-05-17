from unittest.mock import (
    Mock,
    patch,
)

from elsecommon import marshalling
from elsepdm.models import (
    Product,
    ComponentAsset,
    ProductRevision,
    ProductComponent,
    ProductStructure,
)
from elsepublic.exceptions import MissingProductStructureException
from elsecommon.tests.helpers import RouterMock
from elsepdm.tests.test_base_pdm import TestBasePdm
from elsepublic.elsepdm.dto.import_structure_from_obj import (
    ImportStructureFromObjParamsDTO,
)
from elsepublic.elserender.import_from_obj.wrapper.interface import (
    ImportComponentFromObjWrapperOpInterface,
)
from elsepdm.operations.import_from_obj.import_structure_from_obj import (
    ImportStructureFromObjOperation,
)


class TestImportStructureFromObjOperation(TestBasePdm):
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
        test_structure = ProductStructure.objects.create(
            component=test_component,
            name='test_structure',
            export_name='test_str',
            structure='test-str',
        )
        self.test_asset = ComponentAsset.objects.create(
            structure=test_structure,
            brand_id=self.brand.uuid,
            asset_type=ComponentAsset.OBJ_ASSET,
            extension='obj',
        )

        self.import_structure_from_obj_dto = ImportStructureFromObjParamsDTO(
            structure_uuid=test_structure.uuid)
        self.import_missing_structure_from_obj_dto = \
            ImportStructureFromObjParamsDTO(
                structure_uuid=self.fake_uuid,
            )

        self.router_mock = RouterMock()
        self.router_mock[ImportComponentFromObjWrapperOpInterface] = Mock(
            spec=marshalling.ElseOperation)
        self.import_component_from_obj_wrapper_patch = patch(
            'elsepdm.operations.import_from_obj.'
            'import_structure_from_obj.Router',
            new=self.router_mock,
        )

        self.import_structure_from_obj_op = ImportStructureFromObjOperation()

    def test_import_structure_from_obj(self):
        """
        Test import structure from obj
        """
        with self.import_component_from_obj_wrapper_patch:
            import_result = self.import_structure_from_obj_op(
                self.import_structure_from_obj_dto)
        self.assertIsNone(import_result)
        import_component_wrapper_mock = \
            self.router_mock[ImportComponentFromObjWrapperOpInterface]
        self.assertEqual(import_component_wrapper_mock.call_count, 1)

        dto, context = import_component_wrapper_mock.call_args
        dam_asset_info = dto[0].elements[0].dam_asset_info
        self.assertEqual(dam_asset_info.dam_uuid, self.test_asset.dam_uuid)
        self.assertEqual(dam_asset_info.filename, self.test_asset.filename)
        self.assertEqual(dam_asset_info.size, str(self.test_asset.size))
        self.assertEqual(dam_asset_info.extension, self.test_asset.extension)
        self.assertEqual(
            dam_asset_info.brand_id, str(
                self.test_asset.brand_id))
        self.assertEqual(dam_asset_info.url, self.test_asset.url)
        self.assertEqual(dam_asset_info.state, self.test_asset.state)
        self.assertEqual(
            dam_asset_info.resource_type,
            self.test_asset.resource_type)
        self.assertEqual(dam_asset_info.meta_info, self.test_asset.meta_info)

        self.assertEqual(
            context['structure_uuid'],
            self.import_structure_from_obj_dto.structure_uuid)

    def test_import_missing_structure_from_obj(self):
        """
        Test import missing structure from obj
        """
        with self.import_component_from_obj_wrapper_patch:
            with self.assertRaises(MissingProductStructureException):
                self.import_structure_from_obj_op(
                    self.import_missing_structure_from_obj_dto)

        validate_manifest_correct_mock = \
            self.router_mock[ImportComponentFromObjWrapperOpInterface]
        self.assertFalse(validate_manifest_correct_mock.called)
