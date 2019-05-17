from elsecommon import marshalling
from elsepublic.exceptions import MissingProductException
from elsepdm.models import (
    Product,
    ProductRevision,
)
from elsepublic.elsepdm.dto.create_product_revision import (
    CreateProductRevisionParams,
    CreateProductRevisionResult,
)
from elsepublic.elsepdm.serializers.create_product_revision import (
    CreateProductRevisionParamsSerializer,
    CreateProductRevisionResultSerializer,
)


class CreateProductRevisionOperation(marshalling.ElseOperation):
    """
    Operation for create product revision
    """
    expect_serializer_class = CreateProductRevisionParamsSerializer
    expose_serializer_class = CreateProductRevisionResultSerializer

    def __call__(self, data: CreateProductRevisionParams, **context) -> CreateProductRevisionResult:
        """
        Parameters
        ----------
        data : elsepublic.elsepdm.dto.create_product_revision.CreateProductRevisionParams
            Operation input parameters
        context : dict
            context data

        Returns
        -------
        elsepublic.elsepdm.dto.create_product_revision.CreateProductRevisionResult
            Operation result object
        """
        product = Product.objects.filter(uuid=data.product_uuid).first()
        if not product:
            raise MissingProductException

        product_revision = ProductRevision.objects.create(product=product)
        return CreateProductRevisionResult(product_revision_uuid=product_revision.uuid)
