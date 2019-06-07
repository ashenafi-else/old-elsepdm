from elsecommon.marshalling import marshall
from elsepublic.elsepdm.configurations.create import (
    CreateConfigurationParams,
    CreateConfigurationResult,
    CreateConfigurationParamsSerializer,
    CreateConfigurationResultSerializer,
    WrongRevisionStateException,
)
from elsepdm.models import (
    ProductRevision,
    Configuration,
)


@marshall(
    expect=CreateConfigurationParamsSerializer,
    expose=CreateConfigurationResultSerializer,
)
def create_configuration_operation(
        params: CreateConfigurationParams,
        **context,
) -> CreateConfigurationResult:
    """
    Operation for creating a configuration.

    Parameters
    ----------
    params: elsepublic.elsepdm.configurations.create.CreateConfigurationParams
        Input operation parameters
    **context: dict
        Keyword arguments

    Returns
    -------
    elsepublic.elsepdm.configurations.create.CreateConfigurationResult

    Raises
    ------
    elsepublic.elsepdm.configurations.create.WrongRevisionStateException
        When product revision state not in set {
            ProductRevision.READY,
            ProductRevision.PUBLISHING,
            ProductRevision.PUBLISHED,
        }
    """
    product_revision = ProductRevision.objects.get(pk=params.revision_uuid)
    available_states = {
        ProductRevision.READY,
        ProductRevision.PUBLISHING,
        ProductRevision.PUBLISHED,
    }

    if product_revision.state not in available_states:
        raise WrongRevisionStateException

    configuration = Configuration.objects.create(
        product_revision=product_revision,
    )

    return CreateConfigurationResult(
        uuid=configuration.uuid,
    )
