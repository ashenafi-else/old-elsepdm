import logging
from elsecommon import marshalling
from elsedam.models import Brand
from elsepublic.elsedam.dto.remove_brand_operation import (
    RemoveBrandParameters,
    RemoveBrandResult,
)
from elsepublic.elsedam.serializers.remove_brand_operation import (
    RemoveBrandSerializer,
    RemoveBrandResultSerializer,
)

logger = logging.getLogger()


class RemoveBrandOperation(marshalling.ElseOperation):
    """
    Operation for brand removing.

    Attributes
    ----------
    expect_serializer_class : elseserializers.BaseDtoSerializer
        Expect serializer.
    expose_serializer_class : elseserializers.BaseDtoSerializer
        Expose serializer.
    """
    expect_serializer_class = RemoveBrandSerializer
    expose_serializer_class = RemoveBrandResultSerializer

    def __call__(self, data: RemoveBrandParameters, **context) -> RemoveBrandResult:
        brand = Brand.objects.filter(uuid=data.uuid).first()
        if brand:
            brand.delete()
            return RemoveBrandResult(success=True)
        return RemoveBrandResult(success=False)

