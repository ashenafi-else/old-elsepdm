from elsecommon import marshalling
from elsepdm.models import (
    Brand,
    ResourceAsset,
)
from elsepublic.exceptions import (
    MissingBrandException,
    InvalidResourceTypeException,
)
from elsepublic.elsepdm.create_resource import (
    CreateResourceParams,
    CreateResourceResult,
    CreateResourceParamsSerializer,
    CreateResourceResultSerializer,
)
from elsepublic.helpers.asset_dto_to_dict import asset_dto_to_dict


class CreateResourceOperation(marshalling.ElseOperation):
    """
    Operation to create resource asset

    Attributes
    ----------
    expect_serializer_class : elsepublic.elsepdm.create_resource.
    CreateResourceParamsSerializer
        Expect serializer.
    expose_serializer_class : elsepublic.elsepdm.create_resource.
    CreateResourceResultSerializer
        Expose serializer.
    """
    expect_serializer_class = CreateResourceParamsSerializer
    expose_serializer_class = CreateResourceResultSerializer

    def __call__(self, data: CreateResourceParams,
                 **context) -> CreateResourceResult:
        """
        Parameters
        ----------
        data : elsepublic.elsepdm.create_resource.CreateResourceParams
            Operation input parameters
        context : dict
            context data

        Raises
        ------
        MissingBrandException
            if brand with given uuid doesn't exist
        InvalidResourceTypeException
            if resource type passed as a parameter doesn't match any existing

        Returns
        -------
        elsepublic.elsepdm.create_resource.CreateResourceResult
            Operation result object
        """
        brand = Brand.objects.filter(uuid=data.brand_uuid).first()
        if not brand:
            raise MissingBrandException

        if not any(data.resource_type in resource_type
                   for resource_type in ResourceAsset.RESOURCE_TYPES):
            raise InvalidResourceTypeException

        resource = ResourceAsset.objects.create(
            pdm_brand=brand,
            type=data.resource_type,
            asset_type=ResourceAsset.RESOURCE_ASSET,
            name=data.name,
            **asset_dto_to_dict(data.dam_asset_info),
        )

        return CreateResourceResult(resource_uuid=resource.uuid)
