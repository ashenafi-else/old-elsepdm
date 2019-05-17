from elsecommon import marshalling

from elsepublic.elsepdm.serializers.validate_product_manifest import (
    ValidateProductManifestParamsSerializer,
    ValidateProductManifestResultSerializer,
)
from elsepublic.elsepdm.dto.validate_product_manifest import (
    ValidateProductManifestParams,
    ValidateProductManifestResult,
)
from elsepdm.operations.manifest_validation.manifest_validation_utils import (
    get_validation_errors_list,
    validate_materials,
    validate_configurations,
)
from elsepdm.serializers import ProductManifestSerializer


class ValidateProductManifestOperation(marshalling.ElseOperation):
    """
    Operation for validate product manifest

    Attributes
    ----------
    expect_serializer_class : elsepublic.elsepdm.serializers.validate_product_manifest.ValidateProductManifestParamsSerializer
        Expect serializer.
    expose_serializer_class : elsepublic.elsepdm.serializers.validate_product_manifest.ValidateProductManifestResultSerializer
        Expose serializer.
    """
    expect_serializer_class = ValidateProductManifestParamsSerializer
    expose_serializer_class = ValidateProductManifestResultSerializer

    def __call__(self, data: ValidateProductManifestParams, **context) -> ValidateProductManifestResult:
        """
        Parameters
        ----------
        data : elsepublic.elsepdm.dto.validate_product_manifest.ValidateProductManifestParams
            Operation input parameters
        context : dict
            context data

        Returns
        -------
        elsepublic.elsepdm.dto.validate_product_manifest.ValidateProductManifestResult
            Operation result object
        """
        product_manifest_serializer = ProductManifestSerializer(data=data.json_manifest)
        if not product_manifest_serializer.is_valid():
            return ValidateProductManifestResult(
                is_valid=False,
                error_list=get_validation_errors_list(product_manifest_serializer.errors))

        config = data.json_manifest['config']
        materials = config.get('materials')
        available_configurations = config.get('available_configurations')
        default_configuration_path = config.get('default_configuration_path')

        if not any([materials, available_configurations, default_configuration_path]):
            return ValidateProductManifestResult(is_valid=True, error_list=[])

        if not all([materials, available_configurations, default_configuration_path]):
            return ValidateProductManifestResult(is_valid=False, error_list=[
                "Materials, available_configuration or default_configuration_path not found"])

        error_list = []
        components = config['components']
        error_list.extend(validate_materials(components, materials))
        error_list.extend(validate_configurations(components, available_configurations, default_configuration_path))

        return ValidateProductManifestResult(is_valid=not error_list, error_list=error_list)
