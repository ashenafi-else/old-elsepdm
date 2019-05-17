from elsecommon.transports.router import Router
from elsecommon.transports.operation_type import OperationType
from elsecommon.transports.transportabc import TransportABC
from elsedam.tests.test_base_dam import TestBaseDam
from elsepublic.elsedam.dto.create_brand_operation import (
    CreateBrandParameters,
    CreateBrandResult,
)
from elsepublic.elsedam.interfaces.create_brand_operation import CreateBrandOpInterface


class TestCreateBrandOperation(TestBaseDam):
    def setUp(self):
        super().setUp()
        self.create_brand_dto = CreateBrandParameters(brand_external_id='42')
        self.create_existed_brand_dto = CreateBrandParameters(brand_external_id='0')
        Router[CreateBrandOpInterface] = OperationType(expose=False, producer=TransportABC)

    def test_create_brand(self):
        """
        Test create brand
        """
        cre_op = Router[CreateBrandOpInterface.uri]
        create_result = cre_op(self.create_brand_dto)
        self.assertIsInstance(create_result, CreateBrandResult)
        self.assertEqual(create_result.brand_external_id, self.create_brand_dto.brand_external_id)

    def test_create_existed_brand(self):
        """
        Test existed brand creation
        """
        cre_op = Router[CreateBrandOpInterface.uri]
        with self.assertRaises(RuntimeError):
            cre_op(self.create_existed_brand_dto)
