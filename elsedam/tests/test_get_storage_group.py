import os

from elsedam.models import (
    Storage,
    StorageGroup,
)
from django.core.files import File
from elsedam.tests.test_base_dam import TestBaseDam
from elsepublic.elsedam.put_assets.dto import PutAssetParameters
from elsedam.operations.helpers.get_storage_group import get_storage_group


class TestGetStorageGroup(TestBaseDam):
    def setUp(self):
        super().setUp()
        input_file = os.path.join(self.fixtures_path, 'test.png')
        stream = open(input_file, 'rb')
        file = File(stream)
        self.base_asset_for_public = PutAssetParameters(
            filename=os.path.basename(file.name),
            brand_id=self.brand.brand_external_id,
            tags=['a', 'b', 'c'],
            resource_type='type',
            file=stream,
            temporary=False,
        )
        self.base_asset_for_private = PutAssetParameters(
            filename=os.path.basename(file.name),
            brand_id=self.default_brand.brand_external_id,
            tags=['x', 'y', 'z'],
            resource_type='type',
            file=stream,
            temporary=False,
        )
        self.base_asset_for_default_private = PutAssetParameters(
            filename=os.path.basename(file.name),
            brand_id=self.brand.brand_external_id,
            tags=['x', 'y', 'z'],
            resource_type='type',
            file=stream,
            temporary=False,
        )

    def test_get_public_storage_group(self):
        """
        Test get public storage group
        """
        storage_group = get_storage_group(self.base_asset_for_public)
        self.assertTrue(isinstance(storage_group, StorageGroup))
        self.assertEqual(
            storage_group.brand.brand_external_id,
            self.base_asset_for_public.brand_id)
        self.assertEqual(set(storage_group.tags),
                         set(self.base_asset_for_public.tags))

    def test_get_private_storage_group(self):
        """
        Test get private storage group
        """
        storage_group = get_storage_group(self.base_asset_for_private)
        self.assertTrue(isinstance(storage_group, StorageGroup))
        self.assertEqual(
            storage_group.brand.brand_external_id,
            self.base_asset_for_private.brand_id)
        self.assertEqual(
            storage_group.location.storage.storage_type,
            Storage.TYPE_PRIVATE)

    def test_get_default_private_storage_group(self):
        """
        Test get default private storage group
        """
        storage_group = get_storage_group(self.base_asset_for_default_private)
        self.assertTrue(isinstance(storage_group, StorageGroup))
        self.assertTrue(storage_group.brand.is_default)
        self.assertEqual(
            storage_group.location.storage.storage_type,
            Storage.TYPE_PRIVATE)
