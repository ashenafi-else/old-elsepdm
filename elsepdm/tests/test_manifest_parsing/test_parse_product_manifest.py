import os
import json
from elsepdm.tests.test_base_pdm import TestBasePdm
from elsepublic.elsepdm.dto.parse_product_manifest import ParseProductManifestParamsDTO
from elsepdm.operations.manifest_parsing.parse_product_manifest import ParseProductManifestOperation
from elsepdm.models import (
    Product,
    ProductRevision,
    Material,
    ProductComponent,
    ProductStructure,
    ProductElement,
)
from unittest.mock import patch
from elsepublic.exceptions import (
    MissingProductRevisionException,
    NotUpdatedRevisionException,
    MissingMaterialException,
)


class TestParseProductManifestOperation(TestBasePdm):
    def setUp(self):
        super().setUp()

        test_product = Product.objects.create(
            name="test_product1",
            sku="test_pr_1",
            product_hierarchy=self.root,
            description="It's a test product",
            collection=self.collection,
        )
        Material.objects.create(
            name='drummed_leather',
            collection=self.collection,
            external_id=self.fake_uuid,
        )
        Material.objects.create(
            name='suede',
            collection=self.collection,
            external_id=self.fake_uuid,
        )
        with open(os.path.join(self.fixtures_path, 'test_data_full.json')) as f:
            self.single_configuration_product_revision = ProductRevision.objects.create(
                product=test_product,
                state=ProductRevision.UPDATED,
                json_configuration=json.load(f),
            )
        with open(os.path.join(self.fixtures_path, 'test_data_multiple_configurations_for_parse.json')) as f:
            self.multiple_configuration_product_revision = ProductRevision.objects.create(
                product=test_product,
                state=ProductRevision.UPDATED,
                json_configuration=json.load(f),
            )
        with open(os.path.join(self.fixtures_path, 'test_data_multiple_configurations.json')) as f:
            product_revision_with_missing_materials = ProductRevision.objects.create(
                product=test_product,
                state=ProductRevision.UPDATED,
                json_configuration=json.load(f),
            )
        self.not_updated_product_revision = ProductRevision.objects.create(product=test_product)

        self.single_configuration_dto = ParseProductManifestParamsDTO(
            revision_uuid=self.single_configuration_product_revision.uuid,
        )
        self.multiple_configuration_dto = ParseProductManifestParamsDTO(
            revision_uuid=self.multiple_configuration_product_revision.uuid,
        )
        self.not_updated_revision_dto = ParseProductManifestParamsDTO(
            revision_uuid=self.not_updated_product_revision.uuid,
        )
        self.missing_material_revision_dto = ParseProductManifestParamsDTO(
            revision_uuid=product_revision_with_missing_materials.uuid,
        )
        self.missing_revision_dto = ParseProductManifestParamsDTO(
            revision_uuid=self.fake_uuid,
        )

        self.materials = {'drummed_leather', 'suede'}
        self.single_configuration_get_materials_patch = patch(
            'elsepdm.operations.manifest_parsing.parse_product_manifest.get_single_configuration_manifest_materials',
            return_value=self.materials,
        )

        self.op = ParseProductManifestOperation()

    def test_parse_single_configuration_product_manifest(self):
        """
        Test parse single configuration product manifest
        """
        with self.single_configuration_get_materials_patch as mock:
            result = self.op(data=self.single_configuration_dto)
        revision = ProductRevision.objects.get(uuid=self.single_configuration_product_revision.uuid)
        self.assertIsNone(result)
        self.assertEqual(ProductComponent.objects.all().count(), 15)
        self.assertEqual(ProductComponent.objects.first().product, revision)
        self.assertEqual(ProductStructure.objects.all().count(), 15)
        self.assertEqual(ProductStructure.objects.first().component.product, revision)
        self.assertEqual(ProductElement.objects.all().count(), 18)
        self.assertEqual(
            ProductElement.objects.first().structure.component.product,
            self.single_configuration_product_revision,
        )
        self.assertEqual(revision.state, ProductRevision.PARSED)
        self.assertEqual(mock.call_count, 1)

    def test_parse_multiple_configuration_product_manifest(self):
        """
        Test parse multiple configuration product manifest
        """
        with self.single_configuration_get_materials_patch as mock:
            result = self.op(data=self.multiple_configuration_dto)
        revision = ProductRevision.objects.get(uuid=self.multiple_configuration_product_revision.uuid)
        self.assertIsNone(result)
        self.assertEqual(ProductComponent.objects.all().count(), 25)
        self.assertEqual(ProductComponent.objects.first().product, revision)
        self.assertEqual(ProductStructure.objects.all().count(), 25)
        self.assertEqual(
            ProductStructure.objects.first().component.product,
            revision,
        )
        self.assertEqual(ProductElement.objects.all().count(), 56)
        self.assertEqual(
            ProductElement.objects.first().structure.component.product,
            revision,
        )
        self.assertEqual(revision.state, ProductRevision.PARSED)
        self.assertFalse(mock.called)

    def test_parse_product_manifest_with_missing_revision(self):
        """
        Test parse product manifest with missing revision
        """
        with self.assertRaises(MissingProductRevisionException):
            self.op(self.missing_revision_dto)

    def test_parse_not_updated_product_manifest(self):
        """
        Test parse not updated product manifest
        """
        with self.assertRaises(NotUpdatedRevisionException):
            self.op(self.not_updated_revision_dto)

    def test_parse_manifest_with_missing_materials(self):
        """
        Test parse manifest with missing materials
        """
        with self.assertRaises(MissingMaterialException):
            self.op(self.missing_material_revision_dto)
