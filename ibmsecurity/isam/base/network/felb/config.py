import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)

module_uri = "/isam/felb"
requires_modules = None
requires_version = None
requires_model= "Appliance"


def get(isamAppliance, check_mode=False, force=False):
    """
    Retrieving FELB configuration in full
    """
    return isamAppliance.invoke_get("Retrieving FELB configuration in full", module_uri,
                                    requires_modules=requires_modules, requires_version=requires_version, requires_model=requires_model)


def get_config(isamAppliance, check_mode=False, force=False):
    """
    Retrieving FELB configuration
    """
    return isamAppliance.invoke_get("Retrieving FELB configuration", "{0}/configuration".format(module_uri),
                                    requires_modules=requires_modules, requires_version=requires_version, requires_model=requires_model)


def set(isamAppliance, enabled, debug, ha, logging, ssl, services, attributes,
        check_mode=False, force=False):
    """
    Replacing FELB configuration in full
    """

    if force is False:
        update_required, json_data, warnings = _check(isamAppliance, enabled, debug, ha, logging, ssl, services, attributes)

    if force is True or update_required:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_put("Replacing FELB configuration in full", module_uri, json_data,
                                            requires_modules=requires_modules, requires_version=requires_version, requires_model=requires_model)

    return isamAppliance.create_return_object(warnings=warnings)


def _check(isamAppliance, enabled, debug, ha, logging, ssl, services, attributes):

    update_required = False
    ret_obj = get(isamAppliance)
    warnings=ret_obj['warnings']

    json_data = {
        "enabled": enabled,
        "debug": debug,
        "ha": ha,
        "logging": logging,
        "ssl": ssl,
        "services": services,
        "attributes": attributes
    }
    sorted_json_data = ibmsecurity.utilities.tools.json_sort(json_data)
    logger.debug("Sorted input: {0}".format(sorted_json_data))
    sorted_ret_obj = ibmsecurity.utilities.tools.json_sort(ret_obj['data'])
    logger.debug("Sorted existing data: {0}".format(sorted_ret_obj))
    if sorted_ret_obj != sorted_json_data:
        logger.info("Changes detected, update needed.")
        update_required = True

    return update_required, json_data, warnings


def export_file(isamAppliance, filename, check_mode=False, force=False):
    """
    Exporting FELB configuration
    """
    import os.path
    if force is True or os.path.exists(filename) is False:
        if check_mode is False:  # No point downloading a file if in check_mode
            return isamAppliance.invoke_get_file("Exporting FELB configuration", "{}?export=true".format(module_uri),
                                            filename=filename, requires_modules=requires_modules,
                                            requires_version=requires_version, requires_model=requires_model)

    return isamAppliance.create_return_object()


def import_file(isamAppliance, file, check_mode=False, force=False):
    """
    Importing FELB configuration
    """
    if check_mode is True:
        return isamAppliance.create_return_object(changed=True)
    else:
        return isamAppliance.invoke_post_files(description="Importing FELB configuration",
                                               uri=module_uri,
                                               fileinfo=[{
                                                   'file_formfield': 'file',
                                                   'filename': file,
                                                   'mimetype': 'application/octet-stream'
                                               }],
                                               data={},
                                               requires_modules=requires_modules, requires_version=requires_version, requires_model=requires_model)


def compare(isamAppliance1, isamAppliance2):
    """
    Compare FELB configuration between 2 appliances
    """

    ret_obj1 = get(isamAppliance1)
    ret_obj2 = get(isamAppliance2)

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[])
