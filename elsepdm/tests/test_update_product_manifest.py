from elsepdm.tests.test_base_pdm import TestBasePdm
from elsepdm.operations.update_product_manifest import UpdateProductManifestOperation
from elsepublic.elsepdm.interfaces.validate_product_manifest import ValidateProductManifestOpInterface
from elsepublic.elsepdm.dto.validate_product_manifest import ValidateProductManifestResult
from elsepublic.elsepdm.dto.update_product_manifest import UpdateProductManifestParams
from elsecommon.tests.helpers import RouterMock
from elsecommon import marshalling
from unittest.mock import (
    Mock,
    patch,
)
from elsepdm.models import (
    Product,
    ProductRevision,
)
from elsepublic.exceptions import (
    MissingProductRevisionException,
    InvalidManifestException,
)


class TestUpdateProductManifestOperation(TestBasePdm):
    def setUp(self):
        super().setUp()

        test_product = Product.objects.create(
            name="test_product",
            sku="test_pr",
            product_hierarchy=self.root,
            brand=self.brand,
            description="It's a test product")

        test_revision = ProductRevision.objects.create(product=test_product)

        self.update_product_manifest_dto = UpdateProductManifestParams(
                json_manifest={"test_manifest": "test"},
                revision_uuid=test_revision.uuid)

        self.update_missing_revision_product_manifest_dto = UpdateProductManifestParams(
                json_manifest={"test_manifest": "test"},
                revision_uuid=self.fake_uuid)

        self.validate_manifest_result = ValidateProductManifestResult(is_valid=True, error_list=[])
        self.router_correct_mock = RouterMock()
        self.router_correct_mock[ValidateProductManifestOpInterface] = Mock(
            spec=marshalling.ElseOperation,
            return_value=self.validate_manifest_result,
        )
        self.validate_manifest_patch = patch(
            'elsepdm.operations.update_product_manifest.Router',
            new=self.router_correct_mock
        )

        self.validate_incorrect_manifest_result = ValidateProductManifestResult(is_valid=False, error_list=["Error"])
        self.router_incorrect_mock = RouterMock()
        self.router_incorrect_mock[ValidateProductManifestOpInterface] = Mock(
            spec=marshalling.ElseOperation,
            return_value=self.validate_incorrect_manifest_result,
        )
        self.validate_incorrect_manifest_patch = patch(
            'elsepdm.operations.update_product_manifest.Router',
            new=self.router_incorrect_mock
        )

        self.update_op = UpdateProductManifestOperation()

    def test_update_product_manifest(self):
        """
        Test update product manifest
        """
        with self.validate_manifest_patch:
            create_result = self.update_op(self.update_product_manifest_dto)
        self.assertIsNone(create_result)
        validate_manifest_correct_mock = self.router_correct_mock[ValidateProductManifestOpInterface.uri]
        self.assertEqual(validate_manifest_correct_mock.call_count, 1)

        validate_manifest_correct_dto, context = validate_manifest_correct_mock.call_args
        self.assertEqual(validate_manifest_correct_dto[0].json_manifest, self.update_product_manifest_dto.json_manifest)

        revision = ProductRevision.objects.filter(uuid=self.update_product_manifest_dto.revision_uuid).first()
        self.assertEqual(revision.state, ProductRevision.UPDATED)
        self.assertEqual(revision.json_configuration, self.update_product_manifest_dto.json_manifest)

    def test_update_missing_revision_product_manifest(self):
        """
        Test update missing revision product manifest
        """
        with self.validate_manifest_patch:
            with self.assertRaises(MissingProductRevisionException):
                self.update_op(self.update_missing_revision_product_manifest_dto)

        validate_manifest_correct_mock = self.router_correct_mock[ValidateProductManifestOpInterface.uri]
        self.assertFalse(validate_manifest_correct_mock.called)

    def test_update_product_invalid_manifest(self):
        """
        Test update missing revision product manifest
        """
        with self.validate_incorrect_manifest_patch:
            with self.assertRaises(InvalidManifestException):
                self.update_op(self.update_product_manifest_dto)

        validate_manifest_incorrect_mock = self.router_incorrect_mock[ValidateProductManifestOpInterface.uri]
        self.assertEqual(validate_manifest_incorrect_mock.call_count, 1)

        validate_manifest_incorrect_dto, context = validate_manifest_incorrect_mock.call_args
        self.assertEqual(validate_manifest_incorrect_dto[0].json_manifest,
                         self.update_product_manifest_dto.json_manifest)
