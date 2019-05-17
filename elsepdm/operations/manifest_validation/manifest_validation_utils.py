def get_validation_errors_list(error, res=''):
    """
    Function which transforms serializer errors into a list

    Parameters
    ----------
    error : dict or list or str
        error object to transform
    res : str, optional
        string which contains the location of an error object

    Returns
    -------
    list
        List of errors

    """
    if not error:
        return []

    if isinstance(error, list):
        error_list = []
        for error_index, err in enumerate(error):
            error_list.extend(get_validation_errors_list(err, '{} {!s}'.format(res, error_index)))
        return error_list

    elif isinstance(error, dict):
        error_list = []
        for field_name, err in error.items():
            error_list.extend(get_validation_errors_list(err, '{} {!s}'.format(res, field_name)))
        return error_list

    else:
        return [res.rstrip('0123456789') + error]


def collect_element_materials(components):
    """
    Function which collects materials in elements of component's revisions

    Parameters
    ----------
    components : list
        list of components

    Returns
    -------
    set
        Set of materials

    """
    elements_set = set()
    for component in components:
        for structure in component['structures']:
            for element in structure['elements']:
                materials = element.get('materials', {})
                elements_set.update(materials)

    return elements_set


def validate_materials(components, materials):
    """
    Function that checks if all materials in elements are found in materials list

    Parameters
    ----------
    components : list
        list of components
    materials : list
        list of materials

    Returns
    -------
    list
        List of errors found

    """
    error_list = []

    element_materials = collect_element_materials(components)
    for element_material in element_materials:
        if element_material not in materials:
            error_list.append("Material {} is not found in materials".format(element_material))

    return error_list


def collect_component_structures(components):
    """
    Function which collects structures in components

    Parameters
    ----------
    components : list
        list of components

    Returns
    -------
    dict
        Dict with component names as keys and lists of structures as values

    """
    component_structures = {}

    for component in components:
        structures_name_list = []
        for structure in component["structures"]:
            structures_name_list.append(structure["structure"])
        component_structures[component["component"]] = structures_name_list

    return component_structures


def validate_configurations(components, available_configurations, default_configuration_path):
    """
    Function which checks if all configurations are attainable and
    default configuration is in available configurations

    Parameters
    ----------
    components : list
        list of components
    available_configurations : list
        list of available configurations
    default_configuration_path : str
        string which represents sefault configuration path

    Returns
    -------
    list
        List of errors found

    """
    error_list = []
    component_structures = collect_component_structures(components)

    for config in available_configurations:
        for config_component, config_structure in config.items():
            if config_structure not in component_structures[config_component] and config_structure != '0':
                error_list.append("Structure {} is not found in component {} as stated in available configurations"
                                  .format(config_structure, config_component))

    default_configuration = dict(p.split(',') for p in default_configuration_path.split(':'))
    if default_configuration not in available_configurations:
        error_list.append("Default configuration not found in available configurations")

    return error_list
