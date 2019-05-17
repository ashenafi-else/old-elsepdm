from elsecommon import marshalling
from elsepdm.models import (
    ComponentAsset,
    ProductStructure,
)
from elsecommon.transports.router import Router
from elsepublic.dto.dam_asset_info import DamAssetInfoDTO
from elsepublic.elsedam.asset_extensions import AssetExtensions
from elsepublic.elsedam.resource_types import ResourceTypes
from elsepublic.elsepdm.import_structure_from_obj import (
    ImportStructureFromObjParams,
    ImportStructureFromObjParamsSerializer,
)
from elsepublic.elserender.import_from_obj import (
    AsyncImportSingleElementDTO,
    AsyncImportObjComponentParams,
    AsyncImportFromObjOpInterface,
)


class ImportStructureFromObjOperation(marshalling.AsyncElseOperation):
    """
    Operation to import from obj file

    Attributes
    ----------
    expect_serializer_class:
        elsepublic.elsepdm.import_structure_from_obj
        .ImportStructureFromObjParamsSerializer
        Expect serializer.
    """
    expect_serializer_class = ImportStructureFromObjParamsSerializer

    async def __call__(
        self,
        data: ImportStructureFromObjParams,
        **context,
    ) -> None:
        """
        Parameters
        ----------
        data:
            elsepublic.elsepdm.import_structure_from_obj
            .ImportStructureFromObjParams
            Operation input parameters
        context: dict
            context data

        Returns
        -------
        None
        """
        structure = ProductStructure.objects.get(uuid=data.structure_uuid)

        elements = []
        elements_assets = structure.assets.filter(
            asset_type=ComponentAsset.MODEL_ASSET,
            resource_type=ResourceTypes.MODEL_GEOMETRY,
            extension=AssetExtensions.OBJ,
        ).values()
        materials_assets = structure.assets.filter(
            asset_type=ComponentAsset.MODEL_ASSET,
            resource_type=ResourceTypes.MODEL_GEOMETRY,
            extension=AssetExtensions.MTL,
        ).values()

        for asset in elements_assets:
            elements.append(AsyncImportSingleElementDTO(
                dam_asset_info=DamAssetInfoDTO(**asset),
                name=structure.name,
            ))
        import_component_from_obj_op = Router[AsyncImportFromObjOpInterface]
        imported = await import_component_from_obj_op(
            AsyncImportObjComponentParams(
                elements=elements,
                materials=[DamAssetInfoDTO(**material_asset) for material_asset in materials_assets]
            ),
            **context,
        )

        structure = ProductStructure.objects.get(uuid=data.structure_uuid)
        ComponentAsset.objects.create(
            asset_type=ComponentAsset.MODEL_ASSET,
            structure=structure,
            resource_type=imported.dam_asset_batch.resource_type,
            dam_uuid=imported.dam_assets[0].uuid,
            filename=imported.dam_assets[0].filename,
            size=imported.dam_assets[0].size,
            extension=imported.dam_assets[0].extension,
            brand_id=imported.dam_assets[0].brand_id,
            url=imported.dam_assets[0].url,
            state=imported.dam_assets[0].state,
            meta_info=imported.dam_assets[0].meta_info,
        )
