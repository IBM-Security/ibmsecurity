import logging
from ibmsecurity.utilities import tools
from io import open

logger = logging.getLogger(__name__)

# URI for this module
uri = "/iam/access/v8/policies"


def get_all(isamAppliance, filter=None, sortBy=None, check_mode=False, force=False):
    """
    Retrieve a list of policies
    """
    return isamAppliance.invoke_get("Retrieve a list of policies",
                                    "{0}/{1}".format(uri, tools.create_query_string(filter=filter, sortBy=sortBy)))


def get(isamAppliance, name, check_mode=False, force=False):
    """
    Retrieve a specific policy
    """
    ret_obj = search(isamAppliance, name=name, check_mode=check_mode, force=force)
    pol_id = ret_obj['data']

    if pol_id == {}:
        logger.info("Policy {0} had no match, skipping retrieval.".format(name))
        return isamAppliance.create_return_object()
    else:
        return _get(isamAppliance, pol_id)


def _get(isamAppliance, pol_id):
    return isamAppliance.invoke_get("Retrieve a specific policy",
                                    "{0}/{1}".format(uri, pol_id))


def export_xacml(isamAppliance, name, filename, check_mode=False, force=False):
    """
    Export XACML for a specific policy
    """
    import os.path
    if force is False:
        ret_obj = get(isamAppliance, name=name, check_mode=check_mode, force=force)

    if force is True or (ret_obj['data'] != {} and os.path.exists(filename) is False):
        if check_mode is False:  # No point downloading a file if in check_mode
            f = open(filename, 'w')
            f.write(ret_obj['data']['policy'])

    return isamAppliance.create_return_object()


def search(isamAppliance, name, force=False, check_mode=False):
    """
    Search policy id by name
    """
    ret_obj = get_all(isamAppliance)
    return_obj = isamAppliance.create_return_object()

    for obj in ret_obj['data']:
        if obj['name'] == name:
            logger.info("Found Policy {0} id: {1}".format(name, obj['id']))
            return_obj['data'] = obj['id']
            return_obj['rc'] = 0

    return return_obj


def set_file(isamAppliance, name, attributesrequired, policy_file, description="",
             dialect="urn:oasis:names:tc:xacml:2.0:policy:schema:os", predefined=False, new_name=None, check_mode=False,
             force=False):
    # Read policy from file and call set()
    with open(policy_file, 'r') as myfile:
        policy = myfile.read().replace('\n', '')
    return set(isamAppliance, name, attributesrequired, policy, description, dialect, predefined, new_name, check_mode,
               force)


def set(isamAppliance, name, attributesrequired, policy, description="",
        dialect="urn:oasis:names:tc:xacml:2.0:policy:schema:os", predefined=False, new_name=None, check_mode=False,
        force=False):
    """
    Creating or Modifying a Policy
    """
    if (search(isamAppliance, name=name))['data'] == {}:
        # Force the add - we already know policy does not exist
        logger.info("Policy {0} had no match, requesting to add new one.".format(name))
        return add(isamAppliance, name, attributesrequired, policy, description, dialect, predefined, check_mode, True)
    else:
        # Update request
        logger.info("Policy {0} exists, requesting to update.".format(name))
        return update(isamAppliance, name, attributesrequired, policy, description, dialect, predefined, new_name,
                      check_mode, force)


def add(isamAppliance, name, attributesrequired, policy, description="",
        dialect="urn:oasis:names:tc:xacml:2.0:policy:schema:os", predefined=False, check_mode=False, force=False):
    """
    Create a new Policy
    """
    if force is False:
        ret_obj = search(isamAppliance, name)

    if force is True or ret_obj['data'] == {}:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            try:
                import json
                json_data = json.loads(policy)[0]
                logger.info("Policy {0} contains full policy export".format(name))
            except:
                logger.info("Policy {0} only contains policy data".format(name))
                json_data = {
                    "name": name,
                    "attributesrequired": attributesrequired,
                    "description": description,
                    "predefined": predefined,
                    "policy": policy,
                    "dialect": dialect
                }

            return isamAppliance.invoke_post("Create a new Policy", uri, json_data)

    return isamAppliance.create_return_object()


def delete(isamAppliance, name, check_mode=False, force=False):
    """
    Delete a Policy
    """
    ret_obj = search(isamAppliance, name, check_mode=check_mode, force=force)
    mech_id = ret_obj['data']

    if mech_id == {}:
        logger.info("Policy {0} not found, skipping delete.".format(name))
    else:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Delete a Policy",
                "{0}/{1}".format(uri, mech_id))

    return isamAppliance.create_return_object()


def update(isamAppliance, name, attributesrequired, policy, description=None,
           dialect="urn:oasis:names:tc:xacml:2.0:policy:schema:os", predefined=False, new_name=None, check_mode=False,
           force=False):
    """
    Update a specified policy
    """
    pol_id, update_required, json_data = _check(isamAppliance, name, attributesrequired, policy, description,
                                                dialect, predefined, new_name)
    if pol_id is None:
        from ibmsecurity.appliance.ibmappliance import IBMError
        raise IBMError("999", "Cannot update data for unknown policy: {0}".format(name))

    if force is True or update_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Update a specified policy",
                "{0}/{1}".format(uri, pol_id), json_data)

    return isamAppliance.create_return_object()


def _check(isamAppliance, name, attributesrequired, policy, description, dialect, predefined, new_name):
    """
    Check and return True if update needed
    """
    update_required = False
    try:
        import json
        json_data = json.loads(policy)[0]
        logger.info("Policy {0} contains full policy export".format(name))
    except:
        logger.info("Policy {0} only contains policy data".format(name))
        json_data = {
            "attributesrequired": attributesrequired,
            "policy": policy,
            "dialect": dialect,
            "predefined": predefined
        }

    ret_obj = get(isamAppliance, name)
    if ret_obj['data'] == {}:
        logger.warning("Policy not found, returning no update required.")
        return None, update_required, json_data
    else:
        pol_id = ret_obj['data']['id']
        if new_name is not None:
            json_data['name'] = new_name
        else:
            json_data['name'] = name
        if description is not None:
            json_data['description'] = description
        else:
            del ret_obj['data']['description']
        del ret_obj['data']['id']
        del ret_obj['data']['userlastmodified']
        del ret_obj['data']['lastmodified']
        del ret_obj['data']['datecreated']
        import ibmsecurity.utilities.tools
        sorted_json_data = ibmsecurity.utilities.tools.json_sort(json_data)
        logger.debug("Sorted input: {0}".format(sorted_json_data))
        sorted_ret_obj = ibmsecurity.utilities.tools.json_sort(ret_obj['data'])
        logger.debug("Sorted existing data: {0}".format(sorted_ret_obj))
        if sorted_ret_obj != sorted_json_data:
            logger.info("Changes detected, update needed.")
            update_required = True

    return pol_id, update_required, json_data


def compare(isamAppliance1, isamAppliance2):
    """
    Compare Policies between two appliances
    """
    ret_obj1 = get_all(isamAppliance1)
    ret_obj2 = get_all(isamAppliance2)

    for obj in ret_obj1['data']:
        del obj['id']
        del obj['userlastmodified']
        del obj['lastmodified']
        del obj['datecreated']
        ret_obj = get(isamAppliance1, obj['name'])
        obj['policy'] = ret_obj['data']['policy']
    for obj in ret_obj2['data']:
        del obj['id']
        del obj['userlastmodified']
        del obj['lastmodified']
        del obj['datecreated']
        ret_obj = get(isamAppliance2, obj['name'])
        obj['policy'] = ret_obj['data']['policy']

    return tools.json_compare(ret_obj1, ret_obj2,
                              deleted_keys=['id', 'userlastmodified', 'lastmodified', 'datecreated'])
