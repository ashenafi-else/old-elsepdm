from elsecommon import marshalling
from elsecommon.transports.router import Router

from elsepublic.elsepdm.dto.update_product_manifest import UpdateProductManifestParams
from elsepublic.elsepdm.dto.validate_product_manifest import ValidateProductManifestParams
from elsepublic.elsepdm.interfaces.validate_product_manifest import ValidateProductManifestOpInterface
from elsepublic.elsepdm.serializers.update_product_manifest import UpdateProductManifestParamsSerializer

from elsepdm.models import ProductRevision

from elsepublic.exceptions import (
    MissingProductRevisionException,
    InvalidManifestException,
)


class UpdateProductManifestOperation(marshalling.ElseOperation):
    """
    Operation to update product manifest

    Attributes
    ----------
    expect_serializer_class : elsepublic.elsepdm.serializers.update_product_manifest.UpdateProductManifestParamsSerializer
        Expect serializer.
    expose_serializer_class : None
        Expose serializer.
    Raises
    ------
    MissingProductRevisionException
        if revision with given uuid doesn't exist
    InvalidManifestException
        if manifest is invalid
    """
    expect_serializer_class = UpdateProductManifestParamsSerializer
    expose_serializer_class = None

    def __call__(self, data: UpdateProductManifestParams, **context) -> None:
        """
        Parameters
        ----------
        data : elsepublic.elsepdm.dto.update_product_manifest.UpdateProductManifestParams
            Operation input parameters
        context : dict
            context data

        Returns
        -------
        None
        """
        revision = ProductRevision.objects.filter(uuid=data.revision_uuid).first()
        if not revision:
            raise MissingProductRevisionException

        validate_manifest_op = Router[ValidateProductManifestOpInterface.uri]
        validate_res = validate_manifest_op(ValidateProductManifestParams(json_manifest=data.json_manifest))
        if not validate_res.is_valid:
            raise InvalidManifestException

        revision.json_configuration = data.json_manifest
        revision.state = ProductRevision.UPDATED
        revision.save()
