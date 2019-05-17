from django.test import TestCase
from unittest.mock import patch
from elsepdm.tests.test_manifest_validation.test_data_for_validation_utils import (
    error_dict,
    available_configurations_correct,
    available_configurations_incorrect,
    default_configuration_path,
    components,
    collect_element_materials_correct,
    collect_element_materials_incorrect,
    materials_correct,
    collect_component_structures_correct,
    element_materials_correct,
)
from elsepdm.operations.manifest_validation.manifest_validation_utils import (
    get_validation_errors_list,
    validate_configurations,
    validate_materials,
    collect_component_structures,
    collect_element_materials,
)


class TestManifestValidationUtils(TestCase):
    def setUp(self):
        self.correct_element_materials_patch = patch(
            'elsepdm.operations.manifest_validation.manifest_validation_utils.collect_element_materials',
            return_value=collect_element_materials_correct)

        self.incorrect_element_materials_patch = patch(
            'elsepdm.operations.manifest_validation.manifest_validation_utils.collect_element_materials',
            return_value=collect_element_materials_incorrect)

        self.configuration_patch = patch(
            'elsepdm.operations.manifest_validation.manifest_validation_utils.collect_component_structures',
            return_value=collect_component_structures_correct)

    def test_get_validation_errors_list(self):
        """
        Test for get_validation_errors_list function
        """
        error_list = get_validation_errors_list(error_dict)
        self.assertIsInstance(error_list, list)
        self.assertEqual(len(error_list), 11)

        error_list = get_validation_errors_list({})
        self.assertEqual(error_list, [])

    def test_validate_configurations(self):
        """
        Test for validate_configurations function
        """
        with self.configuration_patch:
            error_list = validate_configurations([], available_configurations_incorrect, default_configuration_path)
        self.assertIsInstance(error_list, list)
        self.assertEqual(len(error_list), 2)

        with self.configuration_patch:
            error_list = validate_configurations([], available_configurations_correct, default_configuration_path)
        self.assertEqual(error_list, [])

    def test_validate_materials(self):
        """
        Test for validate_materials function
        """
        with self.correct_element_materials_patch:
            error_list = validate_materials([], materials_correct)
        self.assertEqual(error_list, [])

        with self.incorrect_element_materials_patch:
            error_list = validate_materials([], materials_correct)
        self.assertIsInstance(error_list, list)
        self.assertEqual(len(error_list), 2)

    def test_collect_component_structures(self):
        """
        Test for collect_component_structures function
        """
        component_structures = collect_component_structures(components)
        self.assertEqual(component_structures, collect_component_structures_correct)

        component_structures = collect_component_structures([])
        self.assertEqual(component_structures, {})

    def test_collect_element_materials(self):
        """
        Test for collect_element_materials function
        """
        element_materials = collect_element_materials(components)
        self.assertEqual(element_materials, element_materials_correct)

        element_materials = collect_element_materials([])
        self.assertEqual(element_materials, set())

