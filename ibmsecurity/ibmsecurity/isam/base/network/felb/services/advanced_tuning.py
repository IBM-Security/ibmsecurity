import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)

module_uri = "/isam/felb/configuration/services/"
requires_modules = None
requires_versions = None


def add(isamAppliance, service_name, name, value, check_mode=False, force=False):
    """
    Creates a service level attribute
    """
    if force is True or _check_add(isamAppliance, service_name, name, value) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put("Creating a service attribute",
                                            "{0}{1}?uiCalled=True".format(isamAppliance, service_name),
                                            {
                                                "name": name,
                                                "value": value
                                            }, requires_version=requires_versions,
                                            requires_modules=requires_modules)
    else:
        return isamAppliance.create_return_object()


def delete(isamAppliance, service_name, attribute_name, check_mode=False, force=False):
    """
    deletes a service level attribute
    """

    if force is True or _check_delete(isamAppliance, service_name, attribute_name) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete("Deleting a service attribute",
                                               "{0}{1}/attributes/{2}".format(isamAppliance, service_name,
                                                                              attribute_name),
                                               requires_version=requires_versions,
                                               requires_modules=requires_modules)
    else:
        return isamAppliance.create_return_object()


def get(isamAppliance, service_name, attribute_name):
    """
    Retrieving a service attribute
    """

    return isamAppliance.invoke_get("Retrieving a service attribute",
                                    "{0}{1}/attributes/{2}".format(module_uri, service_name, attribute_name,
                                                                   requires_version=requires_versions,
                                                                   requires_modules=requires_modules))


def get_all(isamAppliance, service_name):
    """
    Retrieving service attribute names
    """
    return isamAppliance.invoke_get("Retrieving service attribute names",
                                    "{0}{1}/attributes?includeAllValues=true".format(isamAppliance, service_name),
                                    requires_version=requires_versions,
                                    requires_modules=requires_modules)  # TODO REST api matches call used in appliance, returns "failed to parse"


def update(isamAppliance, service_name, attribute_name, attribute_value, check_mode=False, force=False):
    """
    Updating a service attribute
    """
    if force is True or _check_add(isamAppliance, service_name, attribute_name) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put("Updating a service attribute",
                                            "{0}{1}/attributes/{2}".format(module_uri, service_name, attribute_name),
                                            {
                                                "value": attribute_value
                                            },
                                            requires_modules=requires_modules, requires_version=requires_versions)
    else:
        return isamAppliance.create_return_object()


def set(isamAppliance, service_name, attribute_name, attribute_value, check_mode=False, force=False):
    """
    Determines if add or update is called
    """
    try:
        check_obj = get(isamAppliance, service_name, attribute_name)
    except:
        logger.warning("The attribute does not exist")
        return add(isamAppliance, service_name, attribute_name, attribute_value, check_mode, force)

    return update(isamAppliance, service_name, attribute_name, attribute_value, check_mode, force)


def compare(isamAppliance1, isamAppliance2):
    """
    Compare configuration between two appliances
    """
    ret_obj1 = get(isamAppliance1)
    ret_obj2 = get(isamAppliance2)

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[])


def _check_add(isamAppliance, service_name, name, value):
    """
    idempotency test for add function
    """
    check_obj = {}
    # check to see if attribute under service name exist, return True if it doesnt exist
    try:
        check_obj = get(isamAppliance, service_name, name)
    except:
        return True

    if check_obj['data']['value'] != value:
        return True
    else:
        return False


def _check_delete(isamAppliance, service_name, attribute_name):
    """
    Checks to see if attribute getting deleted exists
    """
    try:
        check_obj = get(isamAppliance, service_name, attribute_name)
    except:
        return False

    return True
