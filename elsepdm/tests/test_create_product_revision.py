from elsepdm.tests.test_base_pdm import TestBasePdm
from elsepdm.models import (
    Product,
    ProductRevision,
)

from elsecommon.transports.router import Router
from elsecommon.transports.operation_type import OperationType
from elsecommon.transports.transportabc import TransportABC

from elsepublic.elsepdm.interfaces.create_product_revision import CreateProductRevisionOpInterface
from elsepublic.elsepdm.dto.create_product_revision import (
    CreateProductRevisionParams,
    CreateProductRevisionResult,
)


class TestCreateProductRevisionOperation(TestBasePdm):
    def setUp(self):
        super().setUp()

        test_product1 = Product.objects.create(
            name="test_product1",
            sku="test_pr_1",
            product_hierarchy=self.root,
            brand=self.brand,
            description="It's a test product")

        self.create_product_revision_dto = CreateProductRevisionParams(
            product_uuid=test_product1.uuid)

        self.create_product_revision_with_missing_product_dto = CreateProductRevisionParams(
            product_uuid=self.fake_uuid)

        Router[CreateProductRevisionOpInterface] = OperationType(expose=False, producer=TransportABC)
        self.cre_op = Router[CreateProductRevisionOpInterface.uri]

    def test_create_product_revision(self):
        """
        Test create product revision
        """
        create_result = self.cre_op(self.create_product_revision_dto)

        self.assertIsInstance(create_result, CreateProductRevisionResult)

        new_revision = ProductRevision.objects.filter(uuid=create_result.product_revision_uuid).first()
        self.assertEqual(new_revision.product.uuid, self.create_product_revision_dto.product_uuid)

    def test_create_product_revision_with_missing_product(self):
        """
        Test create product revision with missing product
        """
        with self.assertRaises(RuntimeError):
            self.cre_op(self.create_product_revision_with_missing_product_dto)
