from elsecommon.transports.router import Router
from elsecommon.transports.operation_type import OperationType
from elsecommon.transports.transportabc import TransportABC
from elsedam.models import Brand
from elsedam.tests.test_base_dam import TestBaseDam
from elsepublic.elsedam.dto.remove_brand_operation import (
    RemoveBrandParameters,
    RemoveBrandResult,
)
from elsepublic.elsedam.interfaces.remove_brand_operation import RemoveBrandOpInterface


class TestRemoveBrandOperation(TestBaseDam):
    def setUp(self):
        super().setUp()
        self.remove_brand_dto = RemoveBrandParameters(
            uuid=self.brand.uuid
        )
        self.remove_not_existed_brand_dto = RemoveBrandParameters(
            uuid='c4b9f58e-e825-11e8-9f32-f2801f1b9fd1'
        )
        Router[RemoveBrandOpInterface] = OperationType(expose=False, producer=TransportABC)

    def test_remove_brand(self):
        """
        Test remove brand
        """
        rem_op = Router[RemoveBrandOpInterface.uri]
        remove_result = rem_op(self.remove_brand_dto)
        self.assertIsInstance(remove_result, RemoveBrandResult)
        self.assertTrue(remove_result.success)
        self.assertIsNone(Brand.objects.filter(uuid=self.remove_brand_dto.uuid).first())

    def test_remove_not_existed_brand(self):
        """
        Test remove not existed brand
        """
        rem_op = Router[RemoveBrandOpInterface.uri]
        remove_result = rem_op(self.remove_not_existed_brand_dto)
        self.assertIsInstance(remove_result, RemoveBrandResult)
        self.assertFalse(remove_result.success)
