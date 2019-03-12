import ibmsecurity.utilities.tools
import logging

logger = logging.getLogger(__name__)

module_uri = "/isam/felb/configuration/attributes"
requires_modules = None
requires_version = None


def add(isamAppliance, name, value, check_mode=False, force=False):
    """
    Creates attribute
    """
    if force is True or _check_add(isamAppliance, name, value) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post("Creating an attribute", module_uri,
                                             {
                                                 "name": name,
                                                 "value": value
                                             }, requires_modules=requires_modules, requires_version=requires_version)

    else:
        return isamAppliance.create_return_object()


def set(isamAppliance, name, value=None, check_mode=False, force=False):
    """
    Determines if add or update is called
    """
    try:
        ret_obj = get(isamAppliance, name)
    except:
        return add(isamAppliance, name, value, check_mode, force)

    return update(isamAppliance, name, value, check_mode, force)


def delete(isamAppliance, name, check_mode=False, force=False):
    """
    deletes given attribute
    """
    if force is True or _check_delete(isamAppliance, name) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete("Deleting an attribute", "{0}/{1}".format(module_uri, name),
                                               requires_modules=requires_modules, requires_version=requires_version)
    else:
        return isamAppliance.create_return_object()


def get(isamAppliance, attribute_name):
    """
    Retrieves attribute
    """
    return isamAppliance.invoke_get("Retrieving an attribute", "{0}/{1}".format(module_uri, attribute_name),
                                    requires_modules=requires_modules, requires_version=requires_version)


def get_all(isamAppliance):
    """
    Retrieves all attributes
    """

    return isamAppliance.invoke_get("Retrieving attribute names", "{0}/".format(module_uri),
                                    requires_modules=requires_modules, requires_version=requires_version)


def update(isamAppliance, attribute_name, value, check_mode=False, force=False):
    """
    Updates given attribute
    """

    if force is True or _check(isamAppliance, attribute_name, value) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put("Updating an attribute", "{0}/{1}".format(module_uri, attribute_name),
                                            {
                                                "value": value
                                            }, requires_version=requires_version, requires_modules=requires_modules)

    else:
        return isamAppliance.create_return_object()


def _check(isamAppliance, attribute_name, attribute_value):
    """
    Check for idempotency
    """

    # Error handling to see if attribute exist returns True if attribute doesnt exist
    try:
        temp_obj = get(isamAppliance, attribute_name)
    except:
        return True

    if temp_obj['data']['value'] != attribute_value:
        return True
    else:
        return False


def _check_delete(isamAppliance, attribute_name):
    """
    idempotency check for delete
    """

    # check to see if attribute name exist
    try:
        temp = get(isamAppliance, attribute_name)
    except:
        return False

    return True


def _check_add(isamAppliance, name, value):
    """
    checks add function for idempotency
    """
    check_obj = {}

    try:
        check_obj = get(isamAppliance, name)
    except:

        return True

    return False


def compare(isamAppliance1, isamAppliance2):
    """
    Compare cluster configuration between two appliances
    """
    ret_obj1 = get(isamAppliance1)
    ret_obj2 = get(isamAppliance2)

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[])
