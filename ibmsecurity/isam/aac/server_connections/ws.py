import logging
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

# URI for this module
uri = "/mga/server_connections/ws"
requires_modules = ["mga", "federation"]
requires_version = "9.0.2.1"  # Will change if introduced in an earlier version.


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Retrieving a list of all Web Service connections
    """
    return isamAppliance.invoke_get("Retrieving a list of all Web Service connections",
                                    "{0}/v1".format(uri), requires_modules=requires_modules,
                                    requires_version=requires_version)


def get(isamAppliance, name=None, check_mode=False, force=False):
    """
    Retrieving a Web Service connection
    """
    ret_obj = search(isamAppliance, name=name, force=force)
    id = ret_obj["data"]

    if id == {}:
        logger.info("Web Service connection {0} had no match, skipping retrieval.".format(name))
        return isamAppliance.create_return_object()
    else:
        return isamAppliance.invoke_get("Retrieving a Web Service connection",
                                        "{0}/{1}/v1".format(uri, id),
                                        requires_modules=requires_modules,
                                        requires_version=requires_version)


def search(isamAppliance, name, check_mode=False, force=False):
    """
    Search UUID for named Web Service connection
    """
    ret_obj = get_all(isamAppliance)
    return_obj = isamAppliance.create_return_object()
    return_obj["warnings"] = ret_obj["warnings"]

    for obj in ret_obj['data']:
        if obj['name'] == name:
            logger.info("Found Web Service connection {0} id: {1}".format(name, obj['uuid']))
            return_obj['data'] = obj['uuid']
            return_obj['rc'] = 0

    return return_obj


def add(isamAppliance, name, connection, description='', locked=False, check_mode=False, force=False):
    """
    Creating a Web Service connection
    """
    if (search(isamAppliance, name=name))['data'] == {}:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post(
                "Creating a Web Service connection",
                "{0}/v1".format(uri),
                _create_json(name=name, description=description, locked=locked, connection=connection),
                requires_modules=requires_modules, requires_version=requires_version)

    return isamAppliance.create_return_object()


def delete(isamAppliance, name, check_mode=False, force=False):
    """
    Deleting a Web Service connection
    """
    ret_obj = search(isamAppliance, name, check_mode=check_mode, force=force)
    id = ret_obj["data"]

    if force is True or _check_exists(isamAppliance, name=name) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Deleting a Web Service connection",
                "{0}/{1}/v1".format(uri, id), requires_modules=requires_modules,
                requires_version=requires_version)

    return isamAppliance.create_return_object()


def update(isamAppliance, name, connection, description='', locked=False, new_name=None, ignore_password_for_idempotency=False,
           check_mode=False, force=False):
    """
    Modifying a Web Service connection

    Use new_name to rename the connection
    """
    ret_obj = get(isamAppliance, name)
    warnings = ret_obj["warnings"]

    if ret_obj["data"] == {}:
        warnings.append("Web Service connection {0} not found, skipping update.".format(name))
        return isamAppliance.create_return_object(warnings=warnings)
    else:
        id = ret_obj["data"]["uuid"]

    needs_update = False

    json_data = _create_json(name=name, description=description, locked=locked, connection=connection)
    if new_name is not None:  # Rename condition
        json_data['name'] = new_name

    if force is not True:
        if 'uuid' in ret_obj['data']:
            del ret_obj['data']['uuid']
        if ignore_password_for_idempotency:
            if 'password' in connection:
                warnings.append("Request made to ignore password for idempotency check.")
                connection.pop('password', None)

        sorted_ret_obj = tools.json_sort(ret_obj['data'])
        sorted_json_data = tools.json_sort(json_data)
        logger.debug("Sorted Existing Data:{0}".format(sorted_ret_obj))
        logger.debug("Sorted Desired  Data:{0}".format(sorted_json_data))
        if sorted_ret_obj != sorted_json_data:
            needs_update = True

        if 'password' in connection:
            warnings.append("Since existing password cannot be read - this call will not be idempotent.")
            needs_update = True

    if force is True or needs_update is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_put(
                "Modifying a Web Service connection",
                "{0}/{1}/v1".format(uri, id), json_data, requires_modules=requires_modules,
                requires_version=requires_version, warnings=warnings)

    return isamAppliance.create_return_object(warnings=warnings)


def set(isamAppliance, name, connection, description='', locked=False, new_name=None, ignore_password_for_idempotency=False, check_mode=False, force=False):
    """
    Creating or Modifying a Web Service connection
    """
    if (search(isamAppliance, name=name))['data'] == {}:
        # Force the add - we already know connection does not exist
        return add(isamAppliance=isamAppliance, name=name, connection=connection, description=description,
                   locked=locked, check_mode=check_mode, force=True)
    else:
        # Update request
        return update(isamAppliance=isamAppliance, name=name, connection=connection, description=description,
                      locked=locked, new_name=new_name, ignore_password_for_idempotency=ignore_password_for_idempotency, check_mode=check_mode, force=force)


def _create_json(name, description, locked, connection):
    """
    Create a JSON to be used for the REST API call
    """

    json = {
        "connection": connection,
        "type": "ws",
        "name": name,
        "description": description,
        "locked": locked
    }

    return json


def compare(isamAppliance1, isamAppliance2):
    """
    Compare Web Service connections between two appliances
    """
    ret_obj1 = get_all(isamAppliance1)
    ret_obj2 = get_all(isamAppliance2)

    for obj in ret_obj1['data']:
        del obj['uuid']
    for obj in ret_obj2['data']:
        del obj['uuid']

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=['uuid'])


def _check_exists(isamAppliance, name=None, id=None):
    """
    Check if WS Connection already exists
    """
    ret_obj = get_all(isamAppliance)

    for obj in ret_obj['data']:
        if (name is not None and obj['name'] == name) or (id is not None and obj['uuid'] == id):
            return True

    return False
