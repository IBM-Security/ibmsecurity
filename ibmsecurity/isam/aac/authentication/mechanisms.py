import logging
from ibmsecurity.utilities import tools
from ibmsecurity.isam.aac.authentication import mechanism_types
from ibmsecurity.isam.aac.server_connections import smtp
from ibmsecurity.isam.aac.server_connections import ci
from ibmsecurity.isam.aac.server_connections import ws

logger = logging.getLogger(__name__)

# "uri" variable already used so using a different name
module_uri = "/iam/access/v8/authentication/mechanisms"
requires_modules = ["mga"]
requires_version = "8.0.0.0"


def get_all(isamAppliance, start=None, count=None, filter=None, sortBy=None, check_mode=False, force=False):
    """
    Retrieve a list of authentication mechanisms
    """
    return isamAppliance.invoke_get("Retrieve a list of authentication mechanisms",
                                    "{0}{1}".format(module_uri,
                                                    tools.create_query_string(start=start, count=count, filter=filter,
                                                                              sortBy=sortBy)),
                                    requires_modules=requires_modules, requires_version=requires_version)


def get(isamAppliance, name, check_mode=False, force=False):
    """
    Retrieve a specific authentication mechanism
    """
    ret_obj = search(isamAppliance, name=name, check_mode=check_mode, force=force)
    id = ret_obj['data']

    if id == {}:
        logger.info("Authentication Mechanism {0} had no match, skipping retrieval.".format(name))
        return isamAppliance.create_return_object()
    else:
        return isamAppliance.invoke_get("Retrieve a specific authentication mechanism",
                                        "{0}/{1}".format(module_uri, id),
                                        requires_modules=requires_modules, requires_version=requires_version)


def search(isamAppliance, name, force=False, check_mode=False):
    """
    Search authentication mechanism ID by name
    """
    ret_obj = get_all(isamAppliance)
    return_obj = isamAppliance.create_return_object()

    for obj in ret_obj['data']:
        if obj['name'] == name:
            logger.info("Found Authentication Mechanism {0} id: {1}".format(name, obj['id']))
            return_obj['data'] = obj['id']
            return_obj['rc'] = 0

    return return_obj


def set(isamAppliance, name, uri, description=None, attributes=None, properties=None, predefined=None,
        typeName=None, new_name=None, check_mode=False,
        force=False):
    """
    Creating or Modifying an Authentication Mechanism
    """
    if (search(isamAppliance, name=name))['data'] == {}:
        # Force the add - we already know authentication mechanism does not exist
        logger.info("Authentication Mechanism {0} had no match, requesting to add new one.".format(name))
        return add(isamAppliance, name, uri, description, attributes, properties, predefined, typeName, check_mode,
                   True)
    else:
        # Update request
        logger.info("Authentication Mechanism {0} exists, requesting to update.".format(name))
        return update(isamAppliance, name, uri, description, attributes, properties, predefined, typeName, new_name,
                      check_mode, force)


def add(isamAppliance, name, uri, description="", attributes=None, properties=None, predefined=False,
        typeName=None, check_mode=False, force=False):
    """
    Create a new Authentication Mechanism
    """
    if force is False:
        ret_obj = search(isamAppliance, name)

    if force is True or ret_obj['data'] == {}:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            ret_obj = mechanism_types.search(isamAppliance, typeName)
            if ret_obj['data'] == {}:
                from ibmsecurity.appliance.ibmappliance import IBMError
                raise IBMError("999", "Unable to find Authentication Mechanim Type: {0}".format(typeName))
            else:
                typeId = ret_obj['data']
            json_data = {
                "name": name,
                "uri": uri,
                "description": description,
                "predefined": predefined,
                "typeId": typeId
            }
            if attributes is not None:
                json_data['attributes'] = attributes
            if properties is not None:
                logger.info("Searching for keys to substitute value with uuids")
                for property in properties:
                    id = {}
                    if property['key'] == "EmailMessage.serverConnection":
                        id = smtp.search(isamAppliance, property['value'])['data']
                        logger.info("Found EmailMessage.serverConnection by name[{}] with uuid[{}]".format(property['value'], id))
                    elif property['key'] == "ScimConfig.serverConnection":
                        id = ws.search(isamAppliance, property['value'])['data']
                        logger.info("Found ScimConfig.serverConnection by name[{}] with uuid[{}]".format(property['value'], id))
                    elif property['key'] == "CI.serverConnection":
                        id = ci.search(isamAppliance, property['value'])['data']
                        logger.info("Found CI.serverConnection by name[{}] with uuid[{}]".format(property['value'], id))
                    if id != {}:
                        property['value'] = id
                json_data['properties'] = properties
            return isamAppliance.invoke_post(
                "Create a new Authentication Mechanism", module_uri, json_data,
                requires_modules=requires_modules, requires_version=requires_version)

    return isamAppliance.create_return_object()


def delete(isamAppliance, name, check_mode=False, force=False):
    """
    Delete an Authentication Mechanism
    """
    ret_obj = search(isamAppliance, name, check_mode=check_mode, force=force)
    mech_id = ret_obj['data']

    if mech_id == {}:
        logger.info("Authentication Mechanism {0} not found, skipping delete.".format(name))
    else:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Delete an Authentication Mechanism",
                "{0}/{1}".format(module_uri, mech_id),
                requires_modules=requires_modules, requires_version=requires_version)

    return isamAppliance.create_return_object()


def update(isamAppliance, name, uri, description=None, attributes=None, properties=None, predefined=None,
           typeName=None, new_name=None, check_mode=False, force=False):
    """
    Update a specified authentication mechanism
    """
    mech_id, update_required, json_data = _check(isamAppliance, name, description, attributes, properties, predefined,
                                                 uri, typeName, new_name)
    if mech_id is None:
        from ibmsecurity.appliance.ibmappliance import IBMError
        raise IBMError("999", "Cannot update data for unknown authentication mechanism: {0}".format(name))

    if force is True or update_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Update a specified authentication mechanism",
                "{0}/{1}".format(module_uri, mech_id), json_data,
                requires_modules=requires_modules, requires_version=requires_version)

    return isamAppliance.create_return_object()


def _check(isamAppliance, name, description, attributes, properties, predefined, uri, typeName, new_name):
    """
    Check and return True if update needed

    TODO: Need to check for updated by only checking the attribute and properties that are provided (dont compare all)
    """
    update_required = False
    json_data = {
        "uri": uri
    }
    ret_obj = get(isamAppliance, name)
    if ret_obj['data'] == {}:
        logger.info("Authentication Mechanism not found, returning no update required.")
        return None, update_required, json_data
    else:
        mech_id = ret_obj['data']['id']
        if new_name is not None:
            json_data['name'] = new_name
        else:
            json_data['name'] = name
        if typeName is not None:
            ret_obj_type = mechanism_types.search(isamAppliance, typeName)
            if ret_obj_type['data'] == {}:
                from ibmsecurity.appliance.ibmappliance import IBMError
                raise IBMError("999", "Unable to find Authentication Mechanim Type: {0}".format(typeName))
            else:
                json_data['typeId'] = ret_obj_type['data']
        else:
            del ret_obj['data']['typeId']
        if description is not None:
            json_data['description'] = description
        else:
            del ret_obj['data']['description']
        if predefined is not None:
            json_data['predefined'] = predefined
        else:
            del ret_obj['data']['predefined']
        if attributes is not None:
            json_data['attributes'] = attributes
        else:
            # May not exist so skip any exceptions when deleting
            try:
                del ret_obj['data']['attributes']
            except:
                pass
        if properties is not None:
            logger.info("Searching for keys to substitute value with uuids")
            for property in properties:
                id = {}
                if property['key'] == "EmailMessage.serverConnection":
                    id = smtp.search(isamAppliance, property['value'])['data']
                    logger.info("Found EmailMessage.serverConnection by name[{}] with uuid[{}]".format(property['value'], id))
                elif property['key'] == "ScimConfig.serverConnection":
                    id = ws.search(isamAppliance, property['value'])['data']
                    logger.info("Found ScimConfig.serverConnection by name[{}] with uuid[{}]".format(property['value'], id))
                elif property['key'] == "CI.serverConnection":
                    id = ci.search(isamAppliance, property['value'])['data']
                    logger.info("Found CI.serverConnection by name[{}] with uuid[{}]".format(property['value'], id))
                if id != {}:
                    property['value'] = id
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

    return mech_id, update_required, json_data


def compare(isamAppliance1, isamAppliance2):
    """
    Compare Authentication mechanisms between two appliances
    """
    ret_obj1 = get_all(isamAppliance1)
    ret_obj2 = get_all(isamAppliance2)

    for obj in ret_obj1['data']:
        del obj['id']
        del obj['typeId']
    for obj in ret_obj2['data']:
        del obj['id']
        del obj['typeId']

    return tools.json_compare(ret_obj1, ret_obj2, deleted_keys=['id', 'typeId'])
