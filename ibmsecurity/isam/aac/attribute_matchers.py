import logging
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

# URI for this module
am_uri = "/iam/access/v8/attribute-matchers/"
requires_modules = ["mga"]
requires_version = None


def get_all(isamAppliance, filter=None, sortBy=None, check_mode=False, force=False):
    """
    Retrieve a list of attribute matchers
    """
    return isamAppliance.invoke_get("Retrieve a list of Attribute Matchers",
                                    "{0}/{1}".format(am_uri, tools.create_query_string(filter=filter, sortBy=sortBy)),
                                    requires_modules=requires_modules, requires_version=requires_version)


def get(isamAppliance, description, check_mode=False, force=False):
    """
    Retrieve a specific attribute matcher
    """
    warnings = []
    ret_obj = search(isamAppliance, description=description, check_mode=check_mode, force=force)
    id = ret_obj['data']

    if id == {}:
        warnings.append("Attribute Matcher {0} had no match, skipping retrieval.".format(description))
        return isamAppliance.create_return_object(changed=False, warnings=warnings)
    else:
        return _get(isamAppliance, id)


def _get(isamAppliance, id):
    return isamAppliance.invoke_get("Retrieve a specific Attribute Matcher",
                                    "{0}/{1}".format(am_uri, id))


def search(isamAppliance, description, force=False, check_mode=False):
    """
    Search attribute matcher id by description
    """
    ret_obj = get_all(isamAppliance)
    return_obj = isamAppliance.create_return_object()

    for obj in ret_obj['data']:
        if obj['description'] == description:
            logger.info("Found Attribute Matcher {0} id: {1}".format(description, obj['id']))
            return_obj['data'] = obj['id']
            return_obj['rc'] = 0

    return return_obj


def set(isamAppliance, description, properties, predefined=True, supportedDatatype="None", uri="None", check_mode=False,
        force=False):
    """
    Modifying an Attribute Matcher - Add not supported
    """
    warnings = []
    if (search(isamAppliance, description=description))['data'] == {}:
        # Attribute Matcher doesn't exist, Add is not supported
        warnings.append("Attribute Matcher {0} had no match, Add is not supported.".format(description))
        return isamAppliance.create_return_object(changed=False, warnings=warnings)
    else:
        if (description == "Exact attribute matcher" or description == "JavascriptPIPMatcher"):
            warnings.append(
                "Properties for the Exact Attribute Matcher and the JavaScript PIP Matcher should not be modified.")
            return isamAppliance.create_return_object(changed=False, warnings=warnings)
        else:
            # Update request
            logger.info("Attribute Matcher {0} exists, requesting to update.".format(description))
            return update(isamAppliance, description, properties, check_mode, force)


def update(isamAppliance, description, properties, check_mode=False, force=False):
    """
    Update a specified Attribute Matcher
    """
    id, update_required, json_data = _check(isamAppliance, description, properties)
    if id is None:
        from ibmsecurity.appliance.ibmappliance import IBMError
        raise IBMError("999", "Cannot update data for unknown Attribute Matcher: {0}".format(description))

    if force is True or update_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Update a specified Attribute Matcher",
                "{0}/{1}".format(am_uri, id), json_data)

    return isamAppliance.create_return_object()


def _check(isamAppliance, description, properties):
    """
    Check and return True if update needed
    """
    update_required = False
    ret_obj = get(isamAppliance, description)
    json_data = {}
    if ret_obj['data'] == {}:
        logger.warning("Attribute Matcher not found, returning no update required.")
        return None, update_required, json_data
    else:
        json_data = {
            "properties": properties,
            "predefined": ret_obj['data']['predefined'],
            "supportedDatatype": ret_obj['data']['supportedDatatype'],
            "uri": ret_obj['data']['uri']
        }
        id = ret_obj['data']['id']
        del ret_obj['data']['id']
        # del ret_obj['data']['properties']['id']
        del ret_obj['data']['description']
        count = 0
        for i in ret_obj['data']['properties']:
            del ret_obj['data']['properties'][count]['id']
            count += 1
        import ibmsecurity.utilities.tools
        sorted_json_data = ibmsecurity.utilities.tools.json_sort(json_data)
        logger.debug("Sorted input: {0}".format(sorted_json_data))
        sorted_ret_obj = ibmsecurity.utilities.tools.json_sort(ret_obj['data'])
        logger.debug("Sorted existing data: {0}".format(sorted_ret_obj))
        if sorted_ret_obj != sorted_json_data:
            logger.info("Changes detected, update needed.")
            update_required = True

    return id, update_required, json_data


def compare(isamAppliance1, isamAppliance2):
    """
    Compare Attribute Matchers between two appliances
    """
    ret_obj1 = get_all(isamAppliance1)
    ret_obj2 = get_all(isamAppliance2)
    for obj in ret_obj1['data']:
        del obj['id']
    for obj in ret_obj2['data']:
        del obj['id']

    return tools.json_compare(ret_obj1, ret_obj2, deleted_keys=['id'])
