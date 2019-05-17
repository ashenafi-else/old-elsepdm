from elsecommon import marshalling
from elsepdm.models import (
    Product,
    ProductHierarchy,
    Collection,
)
from elsepublic.elsepdm.dto.create_product import (
    CreateProductParams,
    CreateProductResult,
)
from elsepublic.elsepdm.serializers.create_product import (
    CreateProductParamsSerializer,
    CreateProductResultSerializer,
)
from elsepublic.exceptions import (
    ProductExistsException,
    MissingCollectionException,
    MissingProductGroupException,
)


class CreateProductOperation(marshalling.ElseOperation):
    """
    Operation for create product.

    Raises
    ------
    ProductExistsException
        If product instance already exists.
    MissingCollectionException
        If product collection doesn't exist.
    MissingProductGroupException
        If product group doesn't exist.
    """
    expect_serializer_class = CreateProductParamsSerializer
    expose_serializer_class = CreateProductResultSerializer

    def __call__(self, data: CreateProductParams, **context) -> CreateProductResult:
        """
        Parameters
        ----------
        data : elsepublic.elsepdm.dto.create_product.CreateProductParams
            Operation input parameters
        context : dict
            context data

        Returns
        -------
        elsepublic.elsepdm.dto.create_product.CreateProductResult
            Operation result object
        """
        product_group = ProductHierarchy.objects.filter(uuid=data.product_group_uuid).first()
        if not product_group:
            raise MissingProductGroupException

        collection = Collection.objects.filter(uuid=data.collection_uuid).first()
        if not collection:
            raise MissingCollectionException

        new_product, created = Product.objects.get_or_create(
            sku=data.sku,
            collection=collection,
            product_hierarchy=product_group,
            defaults={
                'name': data.name,
                'description': data.description,
            },
        )
        if not created:
            raise ProductExistsException

        return CreateProductResult(
            uuid=new_product.uuid,
            name=new_product.name,
            sku=new_product.sku,
            collection_uuid=new_product.collection.uuid,
            description=new_product.description,
            product_group_uuid=new_product.product_hierarchy.uuid,
        )
