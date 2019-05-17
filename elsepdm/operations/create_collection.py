from elsecommon import marshalling
from elsepdm.models import (
    Brand,
    Collection,
)
from elsepublic.elsepdm.dto.create_collection import (
    CreateCollectionParams,
    CreateCollectionResult,
)
from elsepublic.elsepdm.serializers.create_collection import (
    CreateCollectionParamsSerializer,
    CreateCollectionResultSerializer,
)
from elsepublic.exceptions import MissingBrandException


@marshalling.marshall(expect=CreateCollectionParamsSerializer, expose=CreateCollectionResultSerializer)
def create_collection_operation(params: CreateCollectionParams, **context) -> CreateCollectionResult:
    """
    Operation to create collection.

    Parameters
    ----------
    params : elsepublic.elsepdm.dto.create_collection.CreateCollectionParams
        Operation input parameters
    context : dict
        context data

    Returns
    -------
    elsepublic.elsepdm.dto.create_collection.CreateCollectionResult
        Operation result object

    Raises
    ------
    MissingBrandException
        If collection brand doesn't exist.
    """

    brand = Brand.objects.filter(brand_external_id=params.brand_uuid).first()

    if not brand:
        raise MissingBrandException

    collection = Collection.objects.create(
        name=params.name,
        brand=brand,
    )
    return CreateCollectionResult(
        uuid=collection.uuid,
        brand_uuid=params.brand_uuid,
        name=params.name,
    )
