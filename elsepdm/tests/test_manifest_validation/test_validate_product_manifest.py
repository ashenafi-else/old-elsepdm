import os
import json
from elsepdm.tests.test_base_pdm import TestBasePdm
from elsepublic.elsepdm.dto.validate_product_manifest import (
    ValidateProductManifestParams,
    ValidateProductManifestResult,
)
from elsepdm.operations.manifest_validation.validate_product_manifest import ValidateProductManifestOperation


class TestValidateProductManifestOperation(TestBasePdm):
    def setUp(self):
        super().setUp()
        with open(os.path.join(self.fixtures_path, 'test_data.json')) as f:
            self.validate_manifest_dto = ValidateProductManifestParams(
                json_manifest=json.load(f))

        with open(os.path.join(self.fixtures_path, 'test_data_full.json')) as f:
            self.validate_full_manifest_dto = ValidateProductManifestParams(
                json_manifest=json.load(f))

        with open(os.path.join(self.fixtures_path, 'test_data_multiple_configurations.json')) as f:
            self.validate_multiple_configuration_manifest_dto = ValidateProductManifestParams(
                json_manifest=json.load(f))

        with open(os.path.join(self.fixtures_path, 'test_incorrect_data.json')) as f:
            self.validate_product_incorrect_manifest_dto = ValidateProductManifestParams(
                json_manifest=json.load(f))

        with open(os.path.join(self.fixtures_path, 'test_incorrect_multiple_configurations_data.json')) as f:
            self.validate_product_incorrect_multiple_configuration_manifest_dto = ValidateProductManifestParams(
                json_manifest=json.load(f))

        self.val_op = ValidateProductManifestOperation()

    def test_validate_product_manifest(self):
        """
        Test validate product manifest
        """
        create_result = self.val_op(data=self.validate_manifest_dto)
        self.assertIsInstance(create_result, ValidateProductManifestResult)
        self.assertTrue(create_result.is_valid)

    def test_validate_product_full_manifest(self):
        """
        Test validate product full manifest
        """
        create_result = self.val_op(self.validate_full_manifest_dto)
        self.assertIsInstance(create_result, ValidateProductManifestResult)
        self.assertTrue(create_result.is_valid)

    def test_validate_multiple_configuration_product_manifest(self):
        """
        Test validate multiple configuration product manifest
        """
        create_result = self.val_op(self.validate_multiple_configuration_manifest_dto)
        self.assertIsInstance(create_result, ValidateProductManifestResult)
        self.assertTrue(create_result.is_valid)

    def test_validate_product_incorrect_manifest(self):
        """
        Test validate product incorrect manifest
        """
        create_result = self.val_op(self.validate_product_incorrect_manifest_dto)
        self.assertIsInstance(create_result, ValidateProductManifestResult)
        self.assertFalse(create_result.is_valid)
        self.assertEqual(len(create_result.error_list), 6)

    def test_validate_product_incorrect_multiple_configurations_manifest(self):
        """
        Test validate product incorrect multiple configuration manifest
        """
        create_result = self.val_op(self.validate_product_incorrect_multiple_configuration_manifest_dto)
        self.assertIsInstance(create_result, ValidateProductManifestResult)
        self.assertFalse(create_result.is_valid)
        self.assertEqual(len(create_result.error_list), 3)

