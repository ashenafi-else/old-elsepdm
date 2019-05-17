import logging
from elsecommon import marshalling
from elsedam.models import Brand
from elsepublic.elsedam.dto.create_brand_operation import (
    CreateBrandParameters,
    CreateBrandResult,
)
from elsepublic.elsedam.serializers.create_brand_operation import (
    CreateBrandSerializer,
    CreateBrandResultSerializer,
)

logger = logging.getLogger()


class CreateBrandOperation(marshalling.ElseOperation):
    """
    Operation for brand creation.

    Attributes
    ----------
    expect_serializer_class : elseserializers.BaseDtoSerializer
        Expect serializer.
    expose_serializer_class : elseserializers.BaseDtoSerializer
        Expose serializer.
    """
    expect_serializer_class = CreateBrandSerializer
    expose_serializer_class = CreateBrandResultSerializer

    def __call__(self, data: CreateBrandParameters, **context) -> CreateBrandResult:
        brand = Brand.objects.create(brand_external_id=data.brand_external_id)
        return CreateBrandResult(
            uuid=brand.uuid,
            brand_external_id=brand.brand_external_id,
        )
