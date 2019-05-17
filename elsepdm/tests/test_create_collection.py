from elsepdm.tests.test_base_pdm import TestBasePdm
from elsepdm.models import Collection

from elsepublic.elsepdm.dto.create_collection import (
    CreateCollectionParams,
    CreateCollectionResult,
)
from elsepdm.operations.create_collection import create_collection_operation
from elsepublic.exceptions import MissingBrandException


class TestCreateCollection(TestBasePdm):
    """Test for create material operation"""

    def setUp(self):
        super().setUp()

        self.collection_name = 'test_collection'
        self.create_collection_dto = CreateCollectionParams(
            name=self.collection_name,
            brand_uuid=self.brand.brand_external_id,
        )

    def test_create_collection(self):
        """
        Test create collection success case
        """

        create_result = create_collection_operation(self.create_collection_dto)
        self.assertIsInstance(create_result, CreateCollectionResult)
        self.assertEqual(create_result.name, self.collection_name)
        collections_count = Collection.objects.filter(name=self.collection_name, brand=self.brand).count()
        self.assertEqual(create_result.brand_uuid, self.brand.brand_external_id)
        self.assertEqual(collections_count, 1)

    def test_create_collection_with_missing_brand(self):
        """
        Test create collection with nonexistent brand
        """
        self.create_collection_dto.brand_uuid = '39636c16-6319-47e2-961c-c084e7c5dbb7'
        with self.assertRaises(MissingBrandException):
            create_collection_operation(self.create_collection_dto)
