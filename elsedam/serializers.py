from elsecommon import models as elsemodels
from elsecommon import serializers as elseserializers
from rest_framework import serializers
from .models import DamAsset
from .models import BaseAsset


class AssetParameters(elsemodels.OpParameters):
    base_asset = elsemodels.Field(BaseAsset)


class Upload(elsemodels.Operation):
    parameters = elsemodels.Field(AssetParameters)


class UploadParametersSerializer(serializers.Serializer):
    class Meta:
        model = AssetParameters
        fields = ('base_asset', )


class BaseAssetSerializer(serializers.Serializer):
    class Meta:
        model = BaseAsset
        fields = ('material', 'created_at', 'material_info', 'status', )


class UploadSerializer(elseserializers.OperationSerializer):
    parameters = UploadParametersSerializer()
    result = BaseAssetSerializer()


class DamAssetParameters(elsemodels.OpParameters):
    dam_asset = elsemodels.Field(DamAsset)


class Remove(elsemodels.Operation):
    parameters = elsemodels.Field(DamAssetParameters)


class RemoveParametersSerializer(serializers.Serializer):
    class Meta:
        model = DamAssetParameters
        fields = ('dam_asset', )


class RemoveSerializer(elseserializers.OperationSerializer):
    parameters = RemoveParametersSerializer()
    result = serializers.BooleanField()
