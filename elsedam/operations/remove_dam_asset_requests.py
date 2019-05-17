from elsecommon import marshalling
from elsepublic.elsedam.dto.remove_dam_asset_requests_operation import (
    RemoveDamAssetRequestsParameters,
    RemoveDamAssetRequestsResult,
)
from elsepublic.elsedam.serializers.remove_dam_asset_requests_operation import (
    RemoveDamAssetRequestsSerializer,
    RemoveDamAssetRequestsResultSerializer,
)
from ..models import DamAssetRequest


class RemoveDamAssetRequestsOperation(marshalling.ElseOperation):
    """
    Operation for upload assets to buffer.

    Attributes
    ----------
    expect_serializer_class : elseserializers.BaseDtoSerializer
        Expect serializer.
    expose_serializer_class : elseserializers.BaseDtoSerializer
        Expose serializer.
    """
    expect_serializer_class = RemoveDamAssetRequestsSerializer
    expose_serializer_class = RemoveDamAssetRequestsResultSerializer

    def __call__(self, data: RemoveDamAssetRequestsParameters, **context) -> RemoveDamAssetRequestsResult:
        requests = DamAssetRequest.objects.filter(pk__in=data.dam_asset_requests)
        buffered_assets = [request.buffered_asset for request in requests]
        requests.delete()
        for buffered_asset in set(buffered_assets):
            if not buffered_asset.requests.all():
                buffered_asset.for_removing = True
                buffered_asset.save()
        return RemoveDamAssetRequestsResult(success=True)
