import logging

logger = logging.getLogger(__name__)

# URI for this module
uri = "/mga/attribute_sources"
requires_modules = ["federation"]
requires_version = "9.0.0.0"


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Retrieve a list of attribute sources
    """
    return isamAppliance.invoke_get("Retrieve a list of attribute sources", uri,
                                    requires_modules=requires_modules,
                                    requires_version=requires_version)


def get(isamAppliance, name, check_mode=False, force=False):
    """
    Retrieve a specific attribute source
    """
    ret_obj = search(isamAppliance, name=name, check_mode=check_mode, force=force)
    id = ret_obj['data']

    if id == {}:
        logger.info("Attribute Source {0} had no match, skipping retrieval.".format(name))
        return isamAppliance.create_return_object()
    else:
        return _get(isamAppliance, id)


def _get(isamAppliance, id):
    """
    Internal function to get data using "id" - used to avoid extra calls

    :param isamAppliance:
    :param id:
    :return:
    """
    return isamAppliance.invoke_get("Retrieve a specific attribute source",
                                    "{}/{}".format(uri, id),
                                    requires_modules=requires_modules,
                                    requires_version=requires_version)


def search(isamAppliance, name, force=False, check_mode=False):
    """
    Search Attribute Source by name
    """
    return_obj = isamAppliance.create_return_object()
    ret_obj = get_all(isamAppliance)
    for obj in ret_obj['data']:
        if obj['name'] == name:
            logger.info("Found Attribute Source {0} - id: {1}".format(name, obj['id']))
            return_obj['data'] = obj['id']

    return return_obj


def set(isamAppliance, name, type, value, properties=None, new_name=None, check_mode=False, force=False):
    """
    Creating or Modifying an Attribute Source
    """
    ret_obj = search(isamAppliance, name)
    as_id = ret_obj['data']

    if as_id == {}:
        # Force the add - we already know attribute source does not exist
        return add(isamAppliance, name, type, value, properties, check_mode, True)
    else:
        # Update request
        return update(isamAppliance, name, type, value, properties, new_name, check_mode, force)


def add(isamAppliance, name, type, value, properties=None, check_mode=False, force=False):
    """
    Create an attribute source
    """
    ret_obj = search(isamAppliance, name, check_mode, force)
    as_id = ret_obj['data']
    if as_id != {}:
        logger.info("Attribute Source {0} already exists.".format(name))

    if force is True or as_id == {}:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            json_data = {
                "name": name,
                "type": type,
                "value": value
            }
            if properties is not None:
                json_data['properties'] = properties
            return isamAppliance.invoke_post(
                "Create an attribute source",
                uri, json_data,
                requires_modules=requires_modules,
                requires_version=requires_version)

    return isamAppliance.create_return_object()


def update(isamAppliance, name, type, value, properties=None, new_name=None, check_mode=False, force=False):
    """
    Update an attribute source
    """
    as_id, update_required, json_data = _check(isamAppliance, name, type, value, properties, new_name)

    if force is True or update_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Update an attribute source",
                "{0}/{1}".format(uri, as_id), json_data,
                requires_modules=requires_modules,
                requires_version=requires_version)

    return isamAppliance.create_return_object()


def _check(isamAppliance, name, type, value, properties, new_name=None):
    """
    Check and return True if update needed
    """
    update_required = False
    json_data = {
        "type": type,
        "value": value
    }
    ret_obj = get(isamAppliance, name)
    if ret_obj['data'] == {}:
        logger.info("Attribute Source not found, returning no update required.")
        return None, update_required, json_data
    else:
        as_id = ret_obj['data']['id']
        if new_name is not None:
            json_data['name'] = new_name
        else:
            json_data['name'] = name
        if properties is not None:
            json_data['properties'] = properties
        else:
            # May not exist so skip any exceptions when deleting
            try:
                del ret_obj['data']['properties']
            except:
                pass
        del ret_obj['data']['id']
        import ibmsecurity.utilities.tools
        sorted_json_data = ibmsecurity.utilities.tools.json_sort(json_data)
        logger.debug("Sorted input: {0}".format(sorted_json_data))
        sorted_ret_obj = ibmsecurity.utilities.tools.json_sort(ret_obj['data'])
        logger.debug("Sorted existing data: {0}".format(sorted_ret_obj))
        if sorted_ret_obj != sorted_json_data:
            logger.info("Changes detected, update needed.")
            update_required = True

    return as_id, update_required, json_data


def delete(isamAppliance, name, check_mode=False, force=False):
    """
    Delete an attribute source
    """
    ret_obj = search(isamAppliance, name, check_mode=check_mode, force=force)
    as_id = ret_obj['data']
    if as_id == {}:
        logger.info("Attribute Source: {0}, no longer exists. Skipping delete.".format(name))
    else:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Delete an attribute source",
                "{0}/{1}".format(uri, as_id),
                requires_modules=requires_modules,
                requires_version=requires_version)

    return isamAppliance.create_return_object()


def compare(isamAppliance1, isamAppliance2):
    """
    Compare Attribute Sources between two appliances
    """
    ret_obj1 = get_all(isamAppliance1)
    ret_obj2 = get_all(isamAppliance2)

    for obj in ret_obj1['data']:
        del obj['id']
    for obj in ret_obj2['data']:
        del obj['id']

    import ibmsecurity.utilities.tools
    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=['id'])
