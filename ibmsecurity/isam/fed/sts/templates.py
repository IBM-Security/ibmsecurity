import logging
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

# URI for this module
uri = "/iam/access/v8/sts/templates"
requires_modules = ['federation']
requires_version = "9.0.1.0"


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Retrieve a list of STS chain templates
    """
    return isamAppliance.invoke_get("Retrieve a list of STS chain templates", uri,
                                    requires_modules=requires_modules,
                                    requires_version=requires_version)


def search(isamAppliance, name, force=False, check_mode=False):
    """
    Search STS Chain by name
    """
    ret_obj = get_all(isamAppliance)
    return_obj = isamAppliance.create_return_object()

    for obj in ret_obj['data']:
        if obj['name'] == name:
            logger.info("Found STS Chain Template {0} id: {1}".format(name, obj['id']))
            return_obj['data'] = obj['id']
            return_obj['rc'] = 0

    return return_obj


def get(isamAppliance, name, check_mode=False, force=False):
    """
    Retrieve a specific STS chain template
    """
    ret_obj = search(isamAppliance, name=name, check_mode=check_mode, force=force)
    id = ret_obj['data']

    if id == {}:
        warnings = ["STS Chain Template {0} had no match, skipping retrieval.".format(name)]
        return isamAppliance.create_return_object(warnings=warnings)
    else:
        return _get(isamAppliance, id)


def _get(isamAppliance, id):
    """
    Internal function to get data using "id" - used to avoid extra calls
    """
    return isamAppliance.invoke_get("Retrieve a specific STS chain template", "{0}/{1}".format(uri, id),
                                    requires_modules=requires_modules,
                                    requires_version=requires_version)


def set(isamAppliance, name, chainItems=[], description=None, new_name=None, check_mode=False,
        force=False):
    """
    Creating or Modifying an STS Chain
    """
    if (search(isamAppliance, name=name))['data'] == {}:
        # Force the add - we already know Chain does not exist
        logger.info("STS Chain template {0} had no match, requesting to add new one.".format(name))
        return add(isamAppliance, name=name, chainItems=chainItems, description=description, check_mode=check_mode,
                   force=True)
    else:
        # Update request
        logger.info("STS Chain template {0} exists, requesting to update.".format(name))
        return update(isamAppliance, name=name, chainItems=chainItems, description=description, new_name=new_name,
                      check_mode=check_mode, force=force)


def _flatten_chain(chainItems):
    """
    Convert chainItems from JSON to a simple string for use in comparison, ignore prefix if any.

    DO NOT Sort the JSON containing chainItems for comparison. Sequence is important! Use this function instead.
    """
    chainItemsString = ''
    for ci in chainItems:
        chainItemsString += ci['id'] + ":" + ci['mode'] + " "

    logger.debug("Flattened String: {0}".format(chainItemsString))

    return chainItemsString


def add(isamAppliance, name, chainItems=[], description=None, check_mode=False, force=False):
    """
    Create an STS chain template
    """
    if force is False:
        ret_obj = search(isamAppliance, name)

    if force is True or ret_obj['data'] == {}:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            json_data = {
                "name": name,
                "chainItems": chainItems
            }
            if description is not None:
                json_data['description'] = description
            return isamAppliance.invoke_post(
                "Create an STS chain template", uri, json_data,
                requires_modules=requires_modules,
                requires_version=requires_version)

    return isamAppliance.create_return_object()


def delete(isamAppliance, name, check_mode=False, force=False):
    """
    Delete a specific STS chain template
    """
    ret_obj = search(isamAppliance, name, check_mode=check_mode, force=force)
    chain_id = ret_obj['data']

    if chain_id == {}:
        logger.info("STS Chain Template {0} not found, skipping delete.".format(name))
    else:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Delete a specific STS chain template",
                "{0}/{1}".format(uri, chain_id),
                requires_modules=requires_modules,
                requires_version=requires_version)

    return isamAppliance.create_return_object()


def update(isamAppliance, name, chainItems=[], description=None, new_name=None, check_mode=False, force=False):
    """
    Update a specific STS chain
    """
    warnings = []
    chain_id, update_required, json_data = _check(isamAppliance, name, chainItems, description, new_name)
    if chain_id is None:
        warnings.append("Cannot update data for unknown STS Chain Template: {0}".format(name))
    else:
        if force is True or update_required is True:
            if check_mode is True:
                return isamAppliance.create_return_object(changed=True)
            else:
                return isamAppliance.invoke_put(
                    "Update a specific STS chain template",
                    "{0}/{1}".format(uri, chain_id), json_data,
                    requires_modules=requires_modules,
                    requires_version=requires_version)

    return isamAppliance.create_return_object(warnings=warnings)


def _check(isamAppliance, name, chainItems, description, new_name=None):
    """
    Check and return True if update needed
    """
    update_required = False
    json_data = {
        "name": name,
        "chainItems": chainItems
    }
    ret_obj = get(isamAppliance, name)
    if ret_obj['data'] == {}:
        logger.info("STS Chain template not found, returning no update required.")
        return None, update_required, json_data
    else:
        chain_id = ret_obj['data']['id']
        if new_name is not None:
            json_data['name'] = new_name
        if description is not None:
            json_data['description'] = description
        if (new_name is not None and ret_obj['data']['name'] != name) or (
                description is not None and ret_obj['data']['description'] != description) or (
                _flatten_chain(chainItems) != _flatten_chain(ret_obj['data']['chainItems'])):
            logger.info("Changes detected, update needed.")
            update_required = True
        else:
            logger.debug("No changes detected.")

    return chain_id, update_required, json_data


def compare(isamAppliance1, isamAppliance2):
    """
    Compare STS Chains Templates between two appliances
    """
    ret_obj1 = get_all(isamAppliance1)
    ret_obj2 = get_all(isamAppliance2)

    for obj in ret_obj1['data']:
        del obj['id']
        for ci in obj['chainItems']:
            del ci['prefix']
    for obj in ret_obj2['data']:
        del obj['id']
        for ci in obj['chainItems']:
            del ci['prefix']

    return tools.json_compare(ret_obj1, ret_obj2, deleted_keys=['id', 'chainItems/prefix'])
