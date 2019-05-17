import os
from elsedam.models import DamAsset
from elsedam.tests.test_base_dam import TestBaseDam


class TestAzureService(TestBaseDam):
    test_path = os.path.dirname(os.path.realpath(__file__))
    fixtures_path = os.path.join(test_path, 'fixtures')
    fixtures_models_path = os.path.join(test_path, 'fixtures', 'common_test_data.json')
    dam_assets_models_path = os.path.join(test_path, 'fixtures', 'dam_assets_data.json')
    fixtures = (fixtures_models_path, dam_assets_models_path)

    def setUp(self):
        super().setUp()
        self.dam_asset = DamAsset.objects.get(uuid='642bbbe6-d21b-11e8-a8d5-f2801f1b9da0')
        self.storage = self.dam_asset.location.storage.child_storage

    def test_azure_service_generate_path(self):
        """
        Test azure service generate_path
        """
        path = self.storage.generate_path(self.dam_asset)
        check_path = '{}/{}/{}/{}{}'.format(
            self.dam_asset.location.path,
            self.dam_asset.batch.resource_type,
            self.dam_asset.batch.uuid,
            self.dam_asset.filename,
            self.dam_asset.extension,
        )
        self.assertEqual(path, check_path)

    def test_azure_service_generate_url(self):
        """
        Test azure service generate_url
        """
        path = '{}/{}/{}/{}{}'.format(
            self.dam_asset.location.path,
            self.dam_asset.batch.resource_type,
            self.dam_asset.batch.uuid,
            self.dam_asset.filename,
            self.dam_asset.extension,
        )
        url = self.storage.generate_url(self.dam_asset)

        check_url = '{}/{}/{}'.format(
            self.storage.domain,
            self.dam_asset.location.child_location.container,
            path,
        )
        self.assertEqual(url, check_url)
