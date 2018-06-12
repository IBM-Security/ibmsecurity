import ibmsecurity.utilities.tools

module_uri="/isam/felb/configuration/attributes"
requires_modules=None
requires_version=None

def create(isamAppliance, name, value, check_mode=False, force=False):
    """
    Creates attribute
    """

    return isamAppliance.invoke_post("Creating Attribute", module_uri,
                                     {
                                         "name": name,
                                         "value": value
                                     })

def delete(isamAppliance, attribute_name, check_mode=False, force=False):
    """
    deletes given attribute
    """

    return isamAppliance.invoke_delete("Deleting Attribute", "{0}/{1}".format(module_uri, attribute_name))

def get(isamAppliance, attribute_name):
    """
    Retrieves attribute
    """

    return isamAppliance.invoke_get("Retrieving Attribute", "{0}/{1}".format(module_uri, attribute_name))


def get_all(isamAppliance):
    """
    Retrieves all attributes
    """
    return isamAppliance.invoke_get("Retrieving Attributes", module_uri)


def update(isamAppliance, attribute_name, value, check_mode=False, force=False):
    """
    Updates given attribute
    """
    change_required=False
    change_required, json_data = _check(isamAppliance, attribute_name, value)

    if force is True or change_required is True:
        return isamAppliance.invoke_put("Updating Attribute", "{0}/{1}".format(module_uri, attribute_name), json_data)

def _check(isamAppliance, attribute_name, attribute_value):
    """
    Check for idempotency
    """
    change_required=False

    json_data = {
        "name": attribute_name,
        "value": attribute_value
    }

    ret_obj = get(isamAppliance, attribute_name)

    sort_json_data = ibmsecurity.utilities.tools.json_sort(json_data)
    sort_ret_obj = ibmsecurity.utilities.tools.json_sort(ret_obj)

    if sort_ret_obj != sort_json_data:
        change_required=True

    return change_required, json_data
