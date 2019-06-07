from elsecommon.marshalling import marshall
from elsepublic.elsepdm.configurations.update import (
    UpdateConfigurationParams,
    UpdateConfigurationParamsSerializer,
    WrongConfigurationStateException,
)
from elsepdm.models import (
    Configuration,
    ConfigurationElement,
)


@marshall(expect=UpdateConfigurationParamsSerializer)
def update_configuration_operation(
        params: UpdateConfigurationParams,
        **context,
) -> None:
    """
    Operation for updating a configuration.

    Parameters
    ----------
    params: elsepublic.elsepdm.configurations.update.UpdateConfigurationParams
        Input operation parameters
    **context: dict
        Keyword arguments

    Returns
    -------
    None

    Raises
    ------
    WrongConfigurationStateException
        When configuration state more than Configuration.PREPARED
    """
    configuration = Configuration.objects.get(pk=params.uuid)
    if configuration.state >= Configuration.PUBLISHING:
        raise WrongConfigurationStateException(configuration.state)

    configuration_elements = [ConfigurationElement(

    ) for element in params.elements]
