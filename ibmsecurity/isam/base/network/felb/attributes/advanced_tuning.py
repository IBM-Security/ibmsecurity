import logging

logger = logging.getLogger(__name__)

module_uri = "/isam/felb/configuration/attributes"
requires_modules = None
requires_version = None


def add(isamAppliance, name, value, check_mode=False, force=False):
    """
    Creates attribute
    """
    if force is True or _check(isamAppliance, name, value) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post("Creating Attribute", module_uri,
                                             {
                                                 "name": name,
                                                 "value": value
                                             }, requires_modules=requires_modules, requires_version=requires_version)

    return isamAppliance.create_return_object()


def delete(isamAppliance, attribute_name, check_mode=False, force=False):
    """
    deletes given attribute
    """
    # TODO Idempotency missing
    if check_mode is True:
        return isamAppliance.create_return_object(changed=True)
    else:
        return isamAppliance.invoke_delete("Deleting Attribute", "{0}/{1}".format(module_uri, attribute_name),
                                           requires_modules=requires_modules, requires_version=requires_version)

    return isamAppliance.create_return_object()


def get(isamAppliance, attribute_name):
    """
    Retrieves attribute
    """
    return isamAppliance.invoke_get("Retrieving Attribute", "{0}/{1}".format(module_uri, attribute_name),
                                    requires_modules=requires_modules, requires_version=requires_version)


def get_all(isamAppliance):
    """
    Retrieves all attributes
    """
    return isamAppliance.invoke_get("Retrieving Attributes", "{0}/".format(module_uri),
                                    requires_modules=requires_modules, requires_version=requires_version)


def update(isamAppliance, attribute_name, value, check_mode=False, force=False):
    """
    Updates given attribute
    """

    if force is True or _check(isamAppliance, attribute_name, value) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put("Updating Attribute", "{0}/{1}".format(module_uri, attribute_name),
                                            {
                                                "value": value
                                            }, requires_version=requires_version, requires_modules=requires_modules)

    return isamAppliance.create_return_object(changed=False)


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


# TODO Create compare function
def compare():
    pass
