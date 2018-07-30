import logging
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

# URI for this module
uri = "/iam/access/v8/risk/profiles/"
requires_modules = ["mga"]
requires_version = None


def get_all(isamAppliance, filter=None, sortBy=None, check_mode=False, force=False):
    """
    Retrieve a list of risk profiles
    """
    return isamAppliance.invoke_get("Retrieve a list of Risk Profiles",
                                    "{0}/{1}".format(uri, tools.create_query_string(filter=filter, sortBy=sortBy)),
                                    requires_modules=requires_modules, requires_version=requires_version)


def get(isamAppliance, name, check_mode=False, force=False):
    """
    Retrieve a specific risk profile
    """
    warnings = []
    ret_obj = search(isamAppliance, name=name, check_mode=check_mode, force=force)
    id = ret_obj['data']

    if id == {}:
        warnings.append("Risk Profile {0} had no match, skipping retrieval.".format(name))
        return isamAppliance.create_return_object(changed=False, warnings=warnings)
    else:
        return _get(isamAppliance, id)


def _get(isamAppliance, id):
    return isamAppliance.invoke_get("Retrieve a specific Risk Profile",
                                    "{0}/{1}".format(uri, id))


def search(isamAppliance, name, force=False, check_mode=False):
    """
    Search risk profile id by name
    """
    ret_obj = get_all(isamAppliance)
    return_obj = isamAppliance.create_return_object()

    for obj in ret_obj['data']:
        if obj['name'] == name:
            logger.info("Found Risk Profile {0} id: {1}".format(name, obj['id']))
            return_obj['data'] = obj['id']
            return_obj['rc'] = 0

    return return_obj


def set(isamAppliance, name, active, description=None, attributes=None, predefined=False, check_mode=False,
        force=False):
    """
    Creating or Modifying a Risk Profile
    """
    warnings = []
    if (search(isamAppliance, name=name))['data'] == {}:
        # Force the add - we already know risk profile does not exist
        logger.info("Risk Profile {0} had no match, requesting to add new one.".format(name))
        return add(isamAppliance, name, active, description, attributes, predefined, check_mode, True)
    else:
        # Update request
        logger.info("Risk Profile {0} exists, requesting to update.".format(name))
        return update(isamAppliance, name, active, description, attributes, predefined, check_mode, force)


def add(isamAppliance, name, active, description=None, attributes=None, predefined=False, check_mode=False,
        force=False):
    """
    Create a new Risk Profile
    """
    if force is False:
        ret_obj = search(isamAppliance, name)

    if force is True or ret_obj['data'] == {}:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            json_data = {
                "name": name,
                "active": active,
                "predefined": predefined
            }
            if attributes is not None:
                json_data['attributes'] = attributes
            if description is not None:
                json_data['description'] = description
            return isamAppliance.invoke_post(
                "Create a new Risk Profile", uri, json_data)

    return isamAppliance.create_return_object()


def update(isamAppliance, name, active, description=None, attributes=None, predefined=False, check_mode=False,
           force=False):
    """
    Update a specified Risk Profile
    """
    id, update_required, json_data = _check(isamAppliance, name, active, description, attributes, predefined)
    if id is None:
        from ibmsecurity.appliance.ibmappliance import IBMError
        raise IBMError("999", "Cannot update data for unknown Risk Profile: {0}".format(name))

    if force is True or update_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Update a specified Risk Profile",
                "{0}/{1}".format(uri, id), json_data)

    return isamAppliance.create_return_object()


def _check(isamAppliance, name, active, description, attributes, predefined):
    """
    Check and return True if update needed
    """
    update_required = False
    ret_obj = get(isamAppliance, name)
    if ret_obj['data'] == {}:
        logger.warning("Risk Profile not found, returning no update required.")
        return None, update_required, json_data
    else:
        if ret_obj['data']['predefined'] is True:
            logger.warning("Predefined Risk Profiles can NOT be updated, returning no update required.")
            return ret_obj['data']['id'], update_required, {}
        else:
            json_data = {
                "name": name,
                "active": active,
                "predefined": predefined
            }
            if attributes is not None:
                json_data['attributes'] = attributes
            else:
                del ret_obj['data']['attributes']
            if description is not None:
                json_data['description'] = description
            else:
                del ret_obj['data']['description']

            id = ret_obj['data']['id']
            del ret_obj['data']['id']
            count = 0
            for i in ret_obj['data']['attributes']:
                del ret_obj['data']['attributes'][count]['name']
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


def delete(isamAppliance, name, check_mode=False, force=False):
    """
    Delete a specified Risk Profile
    """
    ret_obj = get(isamAppliance, name, check_mode=check_mode, force=force)
    prof_id = ret_obj['data']['id']
    predef = ret_obj['data']['predefined']
    if prof_id == {}:
        logger.info("Risk Profile {0} not found, skipping delete.".format(name))
    else:
        if predef is True:
            logger.info("Risk Profile {0} is predefined, skipping delete.".format(name))
        else:
            if check_mode is True:
                return isamAppliance.create_return_object(changed=True)
            else:
                return isamAppliance.invoke_delete(
                    "Delete a Risk Profile",
                    "{0}/{1}".format(uri, prof_id))

    return isamAppliance.create_return_object()


def compare(isamAppliance1, isamAppliance2):
    """
    Compare Risk Profiles between two appliances
    """
    ret_obj1 = get_all(isamAppliance1)
    ret_obj2 = get_all(isamAppliance2)
    for obj in ret_obj1['data']:
        del obj['id']
    for obj in ret_obj2['data']:
        del obj['id']

    return tools.json_compare(ret_obj1, ret_obj2, deleted_keys=['id'])
