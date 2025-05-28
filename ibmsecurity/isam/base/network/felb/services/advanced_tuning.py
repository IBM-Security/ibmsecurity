import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)

module_uri = "/isam/felb/configuration/services/"
requires_modules = None
requires_versions = None
requires_model = "Appliance"


def add(isamAppliance, service_name, name, value, check_mode=False, force=False):
    """
    Creates a service attribute
    """

    check_value, warnings = _check(isamAppliance, service_name, name)
    if force is True or check_value is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_post("Creating a service attribute",
                                             f"{module_uri}{service_name}/attributes",
                                             {
                                                 "name": name,
                                                 "value": value
                                             }, requires_version=requires_versions,
                                             requires_modules=requires_modules, requires_model=requires_model)
    else:
        return isamAppliance.create_return_object(warnings=warnings)


def delete(isamAppliance, service_name, attribute_name, check_mode=False, force=False):
    """
    deletes a service level attribute
    """

    check_value, warnings = _check(isamAppliance, service_name, attribute_name)
    if force is True or check_value is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_delete("Deleting a service attribute",
                                               f"{module_uri}{service_name}/attributes/{attribute_name}",
                                               requires_version=requires_versions,
                                               requires_modules=requires_modules, requires_model=requires_model)
    else:
        return isamAppliance.create_return_object(warnings=warnings)


def get(isamAppliance, service_name, attribute_name):
    """
    Retrieving a service attribute
    """

    return isamAppliance.invoke_get("Retrieving a service attribute",
                                    f"{module_uri}{service_name}/attributes/{attribute_name}",
                                    requires_version=requires_versions,
                                    requires_modules=requires_modules,
                                    requires_model=requires_model)


def get_all(isamAppliance, service_name):
    """
    Retrieving service attribute names
    """
    return isamAppliance.invoke_get("Retrieving service attribute names",
                                    f"{module_uri}{service_name}/attributes?includeAllValues=true",
                                    requires_version=requires_versions,
                                    requires_modules=requires_modules,
                                    requires_model=requires_model)


def update(isamAppliance, service_name, attribute_name, attribute_value, check_mode=False, force=False):
    """
    Updating a service attribute
    """

    check_value, warnings = _check_add(isamAppliance, service_name, attribute_name, attribute_value)

    if force is True or check_value is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_put("Updating a service attribute",
                                            f"{module_uri}{service_name}/attributes/{attribute_name}",
                                            {
                                                "value": attribute_value
                                            },
                                            requires_modules=requires_modules, requires_version=requires_versions,
                                            requires_model=requires_model)
    else:
        return isamAppliance.create_return_object(warnings=warnings)


def set(isamAppliance, service_name, attribute_name, attribute_value, check_mode=False, force=False):
    """
    Determines if add or update is called
    """

    check_value, warnings = _check(isamAppliance, service_name, attribute_name)

    if check_value is False:
        return add(isamAppliance, service_name, attribute_name, attribute_value, check_mode, force)
    else:
        return update(isamAppliance, service_name, attribute_name, attribute_value, check_mode, force)


def compare(isamAppliance1, service_name1, isamAppliance2, service_name2):
    """
    Compare configuration between two appliances
    """
    ret_obj1 = get_all(isamAppliance1, service_name1)
    ret_obj2 = get_all(isamAppliance2, service_name2)

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[])


def _check_add(isamAppliance, service_name, name, value):
    """
    idempotency test for add function
    """
    check_obj = {}
    warnings = ""
    # check to see if attribute under service name exist, return True if it doesnt exist
    try:
        check_obj = get(isamAppliance, service_name, name)
        warnings = check_obj['warnings']
    except:
        return True, warnings

    if 'value' in check_obj['data']:
        if check_obj['data']['value'] != value:
            return True, warnings
        else:
            return False, warnings
    else:
        return False, warnings


def _check(isamAppliance, service_name, attribute_name):
    """
    Checks to see if attribute exists
    """
    warnings = ""
    try:
        check_obj = get(isamAppliance, service_name, attribute_name)
        warnings = check_obj['warnings']
    except:
        return False, warnings

    if check_obj['data'] == {}:
        return False, warnings

    return True, warnings
