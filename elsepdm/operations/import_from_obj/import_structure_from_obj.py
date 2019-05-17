from elsecommon import marshalling
from elsepdm.models import (
    ComponentAsset,
    ProductStructure,
)
from elsepublic.exceptions import MissingProductStructureException
from elsecommon.transports.router import Router
from elsepublic.dto.dam_asset_info import DamAssetInfoDTO
from elsepublic.elsepdm.dto.import_structure_from_obj import (
    ImportStructureFromObjParamsDTO,
)
from elsepublic.elserender.import_from_obj.wrapper.dto import (
    ImportComponentFromObjParamsDTO,
    ImportSingleElementComponentFromObjDTO,
)
from elsepublic.elserender.import_from_obj.wrapper.interface import (
    ImportComponentFromObjWrapperOpInterface,
)
from elsepublic.elsepdm.serializers.import_structure_from_obj import (
    ImportStructureFromObjParamsSerializer,
)


class ImportStructureFromObjOperation(marshalling.ElseOperation):
    """
    Operation to import from obj file

    Attributes
    ----------
    expect_serializer_class : elsepublic.elsepdm.serializers.
    import_structure_from_obj.ImportStructureFromObjParamsSerializer
        Expect serializer.

    Raises
    ------
    MissingProductStructureException
        if structure with given uuid doesn't exist
    """
    expect_serializer_class = ImportStructureFromObjParamsSerializer

    def __call__(
            self,
            data: ImportStructureFromObjParamsDTO,
            **context) -> None:
        """
        Parameters
        ----------
        data : elsepublic.elsepdm.dto.
        import_structure_from_obj.ImportStructureFromObjParamsDTO
            Operation input parameters
        context : dict
            context data

        Returns
        -------
        None
        """
        structure = ProductStructure.objects.filter(
            uuid=data.structure_uuid).first()
        if not structure:
            raise MissingProductStructureException

        elements = []
        assets = structure.assets.filter(
            asset_type=ComponentAsset.OBJ_ASSET).values()
        for asset in assets:
            elements.append(ImportSingleElementComponentFromObjDTO(
                dam_asset_info=DamAssetInfoDTO(**asset),
                name=structure.name,
            ))
        import_component_from_obj_op = \
            Router[ImportComponentFromObjWrapperOpInterface]
        context['structure_uuid'] = data.structure_uuid
        # todo add materials
        import_component_from_obj_op(
            ImportComponentFromObjParamsDTO(
                elements=elements), **context)
