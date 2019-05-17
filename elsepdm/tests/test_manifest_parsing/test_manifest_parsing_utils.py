import os
import json
from elsepdm.tests.test_base_pdm import TestBasePdm
from elsepdm.operations.manifest_parsing.manifest_parsing_utils import get_single_configuration_manifest_materials


class TestManifestValidationUtils(TestBasePdm):
    def setUp(self):
        with open(os.path.join(self.fixtures_path, 'test_data_full.json')) as f:
            self.components = json.load(f)['config']['components']

        self.materials = {
            'shoemaster_boxgrain',
            'metal', 'patent_red',
            'laminate', 'plastic',
            'patent_blue',
            'monton',
        }

    def test_get_single_configuration_manifest_materials(self):
        """
        Test for get_single_configuration_manifest_materials function
        """
        result = get_single_configuration_manifest_materials(self.components)
        self.assertIsInstance(result, set)
        self.assertEqual(result, self.materials)
