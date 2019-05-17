def get_single_configuration_manifest_materials(components):
    """
    Function which extracts materials from components of single configuration manifest

    Parameters
    ----------
    components : dict
        components to get materials from

    Returns
    -------
    set
        Material names
    """
    materials = set()
    for component in components:
        for structure in component['structures']:
            for element in structure['elements']:
                materials.add(element['active_material'])

    return materials
