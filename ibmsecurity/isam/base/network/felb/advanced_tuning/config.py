import logging
from ibmsecurity.utilities import tools


logger = logging.getLogger(__name__)

module_uri = "/isam/felb/configuration/attributes"
requires_modules = None
requires_version = None
requires_model = "Appliance"


def add(isamAppliance, name, value, check_mode=False, force=False):
    """
    Creating an attribute
    """

    check_value, warnings = _check(isamAppliance, name, value)

    if force is True or check_value is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_post("Creating an attribute", module_uri,
                                             {
                                                 "name": name,
                                                 "value": value
                                             }, requires_modules=requires_modules, requires_version=requires_version,
                                             requires_model=requires_model)

    else:
        return isamAppliance.create_return_object(warnings=warnings)


def set(isamAppliance, name, value=None, check_mode=False, force=False):
    """
    Determines if add or update is called
    """
    check_value, warnings = search(isamAppliance, name)

    if check_value is False:
        return add(isamAppliance, name, value, check_mode, force)
    else:
        return update(isamAppliance, name, value, check_mode, force)


def delete(isamAppliance, name, check_mode=False, force=False):
    """
    Deleting an attribute
    """

    check_value, warnings = search(isamAppliance, name)

    if force is True or check_value is not False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_delete("Deleting an attribute", "{0}/{1}".format(module_uri, name),
                                               requires_modules=requires_modules, requires_version=requires_version,
                                               requires_model=requires_model)
    else:
        return isamAppliance.create_return_object(warnings=warnings)


def get(isamAppliance, attribute_name):
    """
    Retrieving an attribute
    """
    return isamAppliance.invoke_get("Retrieving an attribute", "{0}/{1}".format(module_uri, attribute_name),
                                    requires_modules=requires_modules, requires_version=requires_version,
                                    requires_model=requires_model)


def get_all(isamAppliance):
    """
    Retrieving attribute names
    """

    return isamAppliance.invoke_get("Retrieving attribute names", "{0}/".format(module_uri),
                                    requires_modules=requires_modules, requires_version=requires_version,
                                    requires_model=requires_model)


def update(isamAppliance, attribute_name, value, check_mode=False, force=False):
    """
    Updating an attribute
    """

    check_value, warnings = _check(isamAppliance, attribute_name, value)

    if force is True or check_value is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_put("Updating an attribute", "{0}/{1}".format(module_uri, attribute_name),
                                            {
                                                "value": value
                                            }, requires_version=requires_version, requires_modules=requires_modules,
                                            requires_model=requires_model)

    else:
        return isamAppliance.create_return_object(warnings=warnings)


def _check(isamAppliance, attribute_name, attribute_value):
    """
    Check for idempotency
    """
    # Error handling to see if attribute exist returns True if attribute doesnt exist
    check_value = False
    warnings = ""

    try:
        temp_obj = get(isamAppliance, attribute_name)
        warnings = temp_obj['warnings']
    except:
        check_value = True
        return check_value, warnings

    if 'value' in temp_obj['data']:
        if temp_obj['data']['value'] != attribute_value:
            check_value = True
            return check_value, warnings
        else:
            check_value = False
            return check_value, warnings
    else:
        check_value = False
        return check_value, warnings


def search(isamAppliance, attribute_name):
    """
    Check for idempotency
    """
    # Error handling to see if attribute exist returns True if attribute doesnt exist

    ret_obj = False
    warnings = ""

    try:
        ret_obj = get(isamAppliance, attribute_name)
        warnings = ret_obj['warnings']
        return ret_obj, warnings
    except:
        ret_obj = False
        return ret_obj, warnings


def compare(isamAppliance1, isamAppliance2):
    """
    Compare between two appliances
    """


    ret_obj1 = get_all(isamAppliance1)
    ret_obj2 = get_all(isamAppliance2)

    obj1_warnings = ret_obj1['warnings']
    obj2_warnings = ret_obj2['warnings']
    warnings = []

    if "Docker" in obj1_warnings or "Docker" in obj2_warnings:
        warnings.append(obj1_warnings)
        warnings.append(obj2_warnings)
        return isamAppliance1.create_return_object(changed=False, warnings=warnings)

    obj1 = {'rc': 0, 'data': [], 'warnings': []}
    obj2 = {'rc': 0, 'data': [], 'warnings': []}

    for attr in ret_obj1["data"]:
        search_result, warnings = search(isamAppliance=isamAppliance1, attribute_name=attr["name"])
        if search_result is not False:
            value = get(isamAppliance1, attribute_name=attr["name"])
            obj1['data'].append({attr["name"]: value["data"]["value"]})
            obj1['warnings'].append(warnings)

    for attr in ret_obj2["data"]:
        search_result, warnings = search(isamAppliance=isamAppliance2, attribute_name=attr["name"])
        if search_result is not False:
            value = get(isamAppliance2, attribute_name=attr["name"])
            obj2['data'].append({attr["name"]: value["data"]["value"]})
            obj2['warnings'].append(warnings)

    return tools.json_compare(obj1, obj2)
