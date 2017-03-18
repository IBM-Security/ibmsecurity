import logging
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)
artifact_type = "Obligation"

# URI for this module
uri = "/iam/access/v8/obligations"


def get_all(isamAppliance, filter=None, sortBy=None, check_mode=False, force=False):
    """
    Retrieve a list of Obligations
    """
    return isamAppliance.invoke_get("Retrieve a list of obligations",
                                    "{0}/{1}".format(uri, tools.create_query_string(filter=filter, sortBy=sortBy)))


def get(isamAppliance, name, check_mode=False, force=False):
    """
    Retrieve a specific Obligation
    """

    ret_obj = search(isamAppliance, name=name, check_mode=check_mode, force=force)
    artifact_id = ret_obj['data']

    if artifact_id == {}:
        logger.info("Obligation {0} had no match, skipping retrieval.".format(name))
        return isamAppliance.create_return_object()
    else:
        return isamAppliance.invoke_get("Retrieve a specific obligation",
                                        "{0}/{1}".format(uri, artifact_id))


def search(isamAppliance, name, force=False, check_mode=False):
    """
    Search obligation id by name
    """
    ret_obj = get_all(isamAppliance)
    return_obj = isamAppliance.create_return_object()

    for obj in ret_obj['data']:
        if obj['name'] == name:
            logger.info("Found obligation {0} id: {1}".format(name, obj['id']))
            return_obj['data'] = obj['id']
            return_obj['rc'] = 0

    return return_obj


def set(isamAppliance, name, description, obligationURI, parameters=[], type="Obligation", typeId="1", properties=[],
        new_name=None, check_mode=False, force=False):
    """
    Creating or Modifying a Obligation
    """
    ret_obj = search(isamAppliance, name)

    if ret_obj['data'] == {}:
        logger.info('Adding "{1}" as a new {0}'.format(artifact_type, name))
        return add(isamAppliance, name, description, parameters, type, obligationURI, typeId, properties, check_mode,
                   True)
    else:
        logger.info('Update for {0} "{1}"'.format(artifact_type, name))
        return update(isamAppliance, name, description, obligationURI, parameters, type, typeId, properties,
                      new_name, check_mode, force)


def add(isamAppliance, name, description, parameters, type, obligationURI, typeId, properties, check_mode, force):
    """
    Create a new Obligation
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
                "obligationURI": obligationURI,
                "type": type,
                "parameters": parameters,
                "properties": properties,
                "typeId": typeId
            }
            return isamAppliance.invoke_post("Create a new obligation", uri, json_data)

    return isamAppliance.create_return_object()


def update(isamAppliance, name, description, obligationURI, parameters=[], type="Obligation", typeId="1", properties=[],
           new_name=None, check_mode=False, force=False):
    """
    Update a specified Obligation

    """
    artifact_id, update_required, json_data = _check(isamAppliance, name, description, obligationURI, parameters, type,
                                                     typeId, properties, new_name)
    if artifact_id is None:
        from ibmsecurity.appliance.ibmappliance import IBMError
        raise IBMError("999", "Cannot update data for unknown obligation: {0}".format(name))

    if force is True or update_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Update a specified policy set",
                "{0}/{1}".format(uri, artifact_id), json_data)

    return isamAppliance.create_return_object()


def _check(isamAppliance, name, description, obligationURI, parameters, type, typeId, properties,
           new_name):
    """
    Check and return True if update needed
    Added logic to check for 'predefined' objects, which cannot be updated
    """
    update_required = False
    json_data = {
        "name": name,
        "description": description,
        "obligationURI": obligationURI,
        "type": type,
        "parameters": parameters,
        "properties": properties,
        "typeId": typeId
    }

    ret_obj = get(isamAppliance, name);
    if ret_obj['data'] == {}:
        logger.warning(" not found, returning no update required.")
        return None, update_required, json_data
    elif ret_obj['data']['predefined']:
        logger.warning("A predefined {0} cannot be updated, returning no update required.".format(artifact_type))
        return None, update_required, json_data
    else:
        artifact_id = ret_obj['data']['id']
        if new_name is not None:
            json_data['name'] = new_name

        del ret_obj['data']['id']
        del ret_obj['data']['predefined']
        import ibmsecurity.utilities.tools
        sorted_json_data = ibmsecurity.utilities.tools.json_sort(json_data)
        logger.debug("Sorted input: {0}".format(sorted_json_data))
        sorted_ret_obj = ibmsecurity.utilities.tools.json_sort(ret_obj['data'])
        logger.debug("Sorted existing data: {0}".format(sorted_ret_obj))
        if sorted_ret_obj != sorted_json_data:
            logger.info("Changes detected, update needed.")
            update_required = True

    return artifact_id, update_required, json_data


def delete(isamAppliance, name, check_mode=False, force=False):
    """
    Delete an Obligation
    """
    ret_obj = get(isamAppliance, name)

    if ret_obj['data'] == {}:
        logger.info('{0} "{1}" not found, skipping delete.'.format(artifact_type, name))
    elif ret_obj['data']["predefined"]:
        logger.info('{0} "{1}" is predefined, skipping delete.'.format(artifact_type, name))
    else:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            logger.info('Deleting {0} "{1}"'.format(artifact_type, name))
            return isamAppliance.invoke_delete(
                "Delete a Policy Set",
                "{0}/{1}".format(uri, ret_obj['data']['id']))

    return isamAppliance.create_return_object()


def compare(isamAppliance1, isamAppliance2):
    """
    Compare Policy Sets between two appliances
    """
    ret_obj1 = get_all(isamAppliance1)
    ret_obj2 = get_all(isamAppliance2)

    for obj in ret_obj1['data']:
        del obj['id']
    for obj in ret_obj2['data']:
        del obj['id']

    return tools.json_compare(ret_obj1, ret_obj2,
                              deleted_keys=['id'])
