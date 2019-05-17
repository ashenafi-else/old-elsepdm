import logging

from elsecommon import marshalling
from elsecommon.models import Operation
from elsecommon.serializers import OperationSerializer

logger = logging.getLogger()


class PutAssetsErrorHandler(marshalling.ElseOperation):
    """
    Error handler for put assets.

    Attributes
    ----------
    expect_serializer_class : elsecommon.serializers.OperationSerializer
        Expect serializer.
    expose_serializer_class : elsecommon.serializers.OperationSerializer
        Expose serializer.
    """
    expect_serializer_class = OperationSerializer
    expose_serializer_class = OperationSerializer

    def __call__(self, data: Operation, **context) -> Operation:
        """
        Parameters
        ----------
        data : elsecommon.models.Operation
            Operation input parameters
        context : dict
            context data

        Returns
        -------
        elsecommon.models.Operation
        """
        return data
