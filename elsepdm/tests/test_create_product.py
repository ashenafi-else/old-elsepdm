from elsepdm.tests.test_base_pdm import TestBasePdm
from elsepdm.models import (
    Product,
    Collection,
)

from elsecommon.transports.router import Router
from elsecommon.transports.operation_type import OperationType
from elsecommon.transports.transportabc import TransportABC

from elsepublic.elsepdm.interfaces.create_product import CreateProductOpInterface
from elsepublic.elsepdm.dto.create_product import (
    CreateProductParams,
    CreateProductResult,
)


class TestCreateProduct(TestBasePdm):

    def setUp(self):
        super().setUp()
        self.collection = Collection.objects.create(
            name='test',
            brand=self.brand,
        )

        preexisting_product = Product.objects.create(
            name="preexisting_test_product",
            sku="test_pr_2",
            product_hierarchy=self.root,
            collection=self.collection,
            description="It's a preexisting test product",
        )

        self.create_product_dto = CreateProductParams(
            name="test_product1",
            sku="test_pr_1",
            product_group_uuid=self.root.uuid,
            collection_uuid=self.collection.uuid,
            description="It's a test product",
        )

        self.create_product_with_missing_group_dto = CreateProductParams(
            name="test_product2",
            sku="test_pr_2",
            product_group_uuid=self.fake_uuid,
            collection_uuid=self.collection.uuid,
            description="It's an invalid test product",
        )

        self.create_product_with_missing_collection_dto = CreateProductParams(
            name="test_product3",
            sku="test_pr_3",
            product_group_uuid=self.root.uuid,
            collection_uuid=self.fake_uuid,
            description="It's an invalid test product",
        )

        self.create_existing_product_dto = CreateProductParams(
            name=preexisting_product.name,
            sku=preexisting_product.sku,
            product_group_uuid=preexisting_product.product_hierarchy.uuid,
            collection_uuid=preexisting_product.collection.uuid,
            description=preexisting_product.description,
        )

        self.create_modified_existing_product_dto = CreateProductParams(
            name="New test name",
            sku=preexisting_product.sku,
            product_group_uuid=preexisting_product.product_hierarchy.uuid,
            collection_uuid=preexisting_product.collection.uuid,
            description="New test description",
        )

        Router[CreateProductOpInterface] = OperationType(expose=False, producer=TransportABC)
        self.cre_op = Router[CreateProductOpInterface.uri]

    def test_create_product(self):
        """
        Test create product
        """

        create_result = self.cre_op(self.create_product_dto)
        self.assertIsInstance(create_result, CreateProductResult)
        self.assertEqual(create_result.name, self.create_product_dto.name)
        self.assertEqual(create_result.sku, self.create_product_dto.sku)
        self.assertEqual(create_result.product_group_uuid, self.create_product_dto.product_group_uuid)
        self.assertEqual(create_result.collection_uuid, self.create_product_dto.collection_uuid)
        self.assertEqual(create_result.description, self.create_product_dto.description)

    def test_create_product_with_missing_group(self):
        """
        Test create product with missing group
        """
        with self.assertRaises(RuntimeError):
            self.cre_op(self.create_product_with_missing_group_dto)

    def test_create_product_with_missing_collection(self):
        """
        Test create product with missing brand
        """
        with self.assertRaises(RuntimeError):
            self.cre_op(self.create_product_with_missing_collection_dto)

    def test_create_existing_product(self):
        """
        Test create existing product
        """
        with self.assertRaises(RuntimeError):
            self.cre_op(self.create_existing_product_dto)

    def test_create_modified_existing_product(self):
        """
        Test create existing product
        """
        with self.assertRaises(RuntimeError):
            self.cre_op(self.create_modified_existing_product_dto)
