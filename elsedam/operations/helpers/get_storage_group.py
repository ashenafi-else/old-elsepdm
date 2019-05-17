from elsedam.models import (
    StorageGroup,
    Storage,
)


def get_storage_group(base_asset):
    """
    Return the storage group that fits asset according to the tags and brand id. 
    If there is no storage group with asset`s tags - storage group with 
    private storage and asset`s brand id will be returned. If the asset's brand 
    does not contain any private storage - default brand`s private storage group 
    will be returned.
    
    Parameters
    ----------
    base_asset: elsepublic.elsedam.dto.put_assets_operation.PutAssetParameters
    
    Returns
    -------
    elsedam.models.StorageGroup
    """
    storage_group = StorageGroup.objects.filter(
        brand__brand_external_id=base_asset.brand_id,
        tags__contains=base_asset.tags,
        tags__contained_by=base_asset.tags,
    ).first()
    if not storage_group:
        storage_group = StorageGroup.objects.filter(
            brand__brand_external_id=base_asset.brand_id,
            location__storage__storage_type=Storage.TYPE_PRIVATE
        ).first()
    if not storage_group:
        storage_group = StorageGroup.objects.filter(
            brand__is_default=True,
            location__storage__storage_type=Storage.TYPE_PRIVATE
        ).first()
    return storage_group
