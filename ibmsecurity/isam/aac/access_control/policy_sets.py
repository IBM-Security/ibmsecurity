import logging
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

# URI for this module
uri = "/iam/access/v8/policysets"


def get_all(isamAppliance, filter=None, sortBy=None, check_mode=False, force=False):
    """
    Retrieve a list of policy sets
    """
    return isamAppliance.invoke_get("Retrieve a list of policy sets",
                                    "{0}/{1}".format(uri, tools.create_query_string(filter=filter, sortBy=sortBy)))


def get(isamAppliance, name, check_mode=False, force=False):
    """
    Retrieve a specific policy set
    """
    ret_obj = search(isamAppliance, name=name, check_mode=check_mode, force=force)
    pol_id = ret_obj['data']

    if pol_id == {}:
        logger.info("Policy {0} had no match, skipping retrieval.".format(name))
        return isamAppliance.create_return_object()
    else:
        return isamAppliance.invoke_get("Retrieve a specific policy set",
                                        "{0}/{1}".format(uri, pol_id))


def get_policies(isamAppliance, name, check_mode=False, force=False):
    """
    Retrieve policies in a specific policy set
    """
    ret_obj = search(isamAppliance, name=name, check_mode=check_mode, force=force)
    pol_id = ret_obj['data']

    if pol_id == {}:
        logger.info("Policy {0} had no match, skipping retrieval.".format(name))
        return isamAppliance.create_return_object()
    else:
        return isamAppliance.invoke_get("Retrieve policies in a specific policy set",
                                        "{0}/{1}/policies".format(uri, pol_id))


def search(isamAppliance, name, force=False, check_mode=False):
    """
    Search policy set id by name
    """
    ret_obj = get_all(isamAppliance)
    return_obj = isamAppliance.create_return_object()

    for obj in ret_obj['data']:
        if obj['name'] == name:
            logger.info("Found Policy Set {0} id: {1}".format(name, obj['id']))
            return_obj['data'] = obj['id']
            return_obj['rc'] = 0

    return return_obj


def set(isamAppliance, name, policies=None, policyCombiningAlgorithm='denyOverrides', description="", predefined=False,
        new_name=None, check_mode=False, force=False):
    """
    Creating or Modifying a Policy Set

    Note: Please input policies as an array of policy names (it will be converted to id's)
    """
    if (search(isamAppliance, name=name))['data'] == {}:
        # Force the add - we already know policy set does not exist
        logger.info("Policy Set {0} had no match, requesting to add new one.".format(name))
        return add(isamAppliance, name, policies, policyCombiningAlgorithm, description, predefined, check_mode, True)
    else:
        # Update request
        logger.info("Policy Set {0} exists, requesting to update.".format(name))
        return update(isamAppliance, name, policies, policyCombiningAlgorithm, description, predefined, new_name,
                      check_mode, force)


def add(isamAppliance, name, policies=None, policyCombiningAlgorithm='denyOverrides', description="", predefined=False,
        check_mode=False, force=False):
    """
    Create a new Policy Set

    Note: Please input policies as an array of policy names (it will be converted to id's)
    """
    if force is False:
        ret_obj = search(isamAppliance, name)

    if force is True or ret_obj['data'] == {}:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            json_data = {
                "name": name,
                "description": description,
                "predefined": predefined
            }
            if policies is not None:
                json_data['policies'] = _convert_policy_name_to_id(isamAppliance, policies)
            if policyCombiningAlgorithm is not None:
                json_data['policyCombiningAlgorithm'] = policyCombiningAlgorithm
            return isamAppliance.invoke_post(
                "Create a new Policy Set", uri, json_data)

    return isamAppliance.create_return_object()


def _convert_policy_name_to_id(isamAppliance, policies):
    pol_ids = []
    import ibmsecurity.isam.aac.access_control.policies
    for pol_name in policies:
        ret_obj = ibmsecurity.isam.aac.access_control.policies.search(isamAppliance, pol_name)
        pol_id = ret_obj['data']
        if pol_id != {}:
            pol_ids.append(pol_id)
            logger.debug("Converting policy {0} to ID: {1}".format(pol_name, pol_id))
        else:
            logger.warning("Unable to find policy {0}, skipping.".format(pol_name))

    return pol_ids


def _convert_policy_id_to_name(isamAppliance, policies):
    pol_names = []
    import ibmsecurity.isam.aac.access_control.policies
    for pol_id in policies:
        ret_obj = ibmsecurity.isam.aac.access_control.policies._get(isamAppliance, pol_id)
        if ret_obj['data'] != {}:
            pol_name = ret_obj['data']['name']
            pol_names.append(pol_name)
            logger.debug("Converting policy {0} to Name: {1}".format(pol_id, pol_name))
        else:
            logger.warning("Unable to find policy {0}, skipping.".format(pol_id))

    return pol_names


def delete(isamAppliance, name, check_mode=False, force=False):
    """
    Delete a Policy Set
    """
    ret_obj = search(isamAppliance, name, check_mode=check_mode, force=force)
    pol_id = ret_obj['data']

    if pol_id == {}:
        logger.info("Policy Set {0} not found, skipping delete.".format(name))
    else:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Delete a Policy Set",
                "{0}/{1}".format(uri, pol_id))

    return isamAppliance.create_return_object()


def update(isamAppliance, name, policies=None, policyCombiningAlgorithm='denyOverrides', description="",
           predefined=False,
           new_name=None, check_mode=False, force=False):
    """
    Update a specified policy set

    Note: Please input policies as an array of policy names (it will be converted to id's)
    """
    pol_id, update_required, json_data = _check(isamAppliance, name, policies, policyCombiningAlgorithm, description,
                                                predefined, new_name)
    if pol_id is None:
        from ibmsecurity.appliance.ibmappliance import IBMError
        raise IBMError("999", "Cannot update data for unknown policy set: {0}".format(name))

    if force is True or update_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Update a specified policy set",
                "{0}/{1}".format(uri, pol_id), json_data)

    return isamAppliance.create_return_object()


def _check(isamAppliance, name, policies, policyCombiningAlgorithm, description, predefined, new_name):
    """
    Check and return True if update needed
    """
    update_required = False
    json_data = {
        "name": name,
        "description": description,
        "predefined": predefined
    }
    ret_obj = get(isamAppliance, name)
    if ret_obj['data'] == {}:
        logger.warning("Policy Set not found, returning no update required.")
        return None, update_required, json_data
    else:
        pol_id = ret_obj['data']['id']
        if new_name is not None:
            json_data['name'] = new_name
        else:
            json_data['name'] = name
        if policies is not None:
            json_data['policies'] = _convert_policy_name_to_id(isamAppliance, policies)
        else:
            try:
                del ret_obj['data']['policies']
            except:
                pass
        if policyCombiningAlgorithm is not None:
            json_data['policyCombiningAlgorithm'] = policyCombiningAlgorithm
        else:
            try:
                del ret_obj['data']['policyCombiningAlgorithm']
            except:
                pass
        del ret_obj['data']['id']
        del ret_obj['data']['userlastmodified']
        del ret_obj['data']['lastmodified']
        del ret_obj['data']['datecreated']
        # TODO Check if sorting of policies is a valid for comparison (order maybe important!)
        import ibmsecurity.utilities.tools
        sorted_json_data = ibmsecurity.utilities.tools.json_sort(json_data)
        logger.debug("Sorted input: {0}".format(sorted_json_data))
        sorted_ret_obj = ibmsecurity.utilities.tools.json_sort(ret_obj['data'])
        logger.debug("Sorted existing data: {0}".format(sorted_ret_obj))
        if sorted_ret_obj != sorted_json_data:
            logger.info("Changes detected, update needed.")
            update_required = True

    return pol_id, update_required, json_data


def update_policies(isamAppliance, name, policies, action, check_mode=False, force=False):
    """
    Update a specified policy set's policies (add/remove/set)

    Note: Please input policies as an array of policy names (it will be converted to id's)
    """
    pol_id, update_required, json_data = _check_policies(isamAppliance, name, policies, action)

    if pol_id is None:
        from ibmsecurity.appliance.ibmappliance import IBMError
        raise IBMError("999", "Cannot update data for unknown policy set: {0}".format(name))

    if force is True or update_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Update a specified policy set",
                "{0}/{1}/policies{2}".format(uri, pol_id, tools.create_query_string(action=action)), json_data)

    return isamAppliance.create_return_object()


def _check_policies(isamAppliance, name, policies, action):
    update_required = False
    json_data = {}
    pol_ids = []
    ret_obj = get(isamAppliance, name)
    if ret_obj['data'] == {}:
        logger.warning("Policy Set not found, returning no update required.")
        return None, update_required, json_data
    else:
        pol_id = ret_obj['data']['id']
        new_pol_ids = _convert_policy_name_to_id(isamAppliance, policies)
        if action == 'set':
            pol_ids = new_pol_ids
        else:
            for new_pol_id in new_pol_ids:
                if new_pol_id in ret_obj['data']['policies']:
                    exists = True
                else:
                    exists = False
                if action == 'add':
                    if exists:
                        logger.info("Policy ID {0} already exists skipping.".format(new_pol_id))
                    else:
                        pol_ids.append(new_pol_ids)
                        logger.info("Policy ID {0} does not exist, appending to list for additon.".format(new_pol_id))
                elif action == 'delete':
                    if exists:
                        pol_ids.append(new_pol_ids)
                        logger.info("Policy ID {0} exists, appending to list for deletion.".format(new_pol_id))
                    else:
                        logger.info("Policy ID {0} does not exist skipping.")
                else:
                    from ibmsecurity.appliance.ibmappliance import IBMError
                    raise IBMError("999", "Unknown action: {0}.".format(action))

        json_data['policies'] = pol_ids
        return pol_id, update_required, json_data


def compare(isamAppliance1, isamAppliance2):
    """
    Compare Policy Sets between two appliances
    """
    ret_obj1 = get_all(isamAppliance1)
    ret_obj2 = get_all(isamAppliance2)

    for obj in ret_obj1['data']:
        del obj['id']
        del obj['userlastmodified']
        del obj['lastmodified']
        del obj['datecreated']
        obj['policies'] = _convert_policy_id_to_name(isamAppliance1, obj['policies'])
    for obj in ret_obj2['data']:
        del obj['id']
        del obj['userlastmodified']
        del obj['lastmodified']
        del obj['datecreated']
        obj['policies'] = _convert_policy_id_to_name(isamAppliance2, obj['policies'])

    return tools.json_compare(ret_obj1, ret_obj2,
                              deleted_keys=['id', 'userlastmodified', 'lastmodified', 'datecreated'])
