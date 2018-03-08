import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)

# URI for this module
uri = "/mga/server_connections/ws"
requires_modules = ["mga", "federation"]
requires_version = "9.0.2.1"    # Will change if introduced in an earlier version.


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
    ret_obj = _get_id(isamAppliance, name=name)
    id = ret_obj['data']

    if id == {}:
        return isamAppliance.create_return_object()
    else:
        return isamAppliance.invoke_get("Retrieving a Web Service connection",
                                        "{0}/{1}/v1".format(uri, id),
                                        requires_modules=requires_modules,
                                        requires_version=requires_version)


def set(isamAppliance, name, connection, description='', locked=False, servers=None,
        check_mode=False, force=False):
    """
    Creating or Modifying a Web Service connection
    """
    if _check_exists(isamAppliance, name=name) is False:
        # Force the add - we already know connection does not exist
        return add(isamAppliance, name, connection, description, locked, servers, check_mode, True)
    else:
        # Update request
        return update(isamAppliance, connection, description, locked, servers, name, None,
                      check_mode, force)


def add(isamAppliance, name, connection, description='', locked=False, servers=None,
        check_mode=False, force=False):
    """
    Creating a Web Service connection
    """
    if force is True or _check_exists(isamAppliance, name=name) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post(
                "Creating a Web Service connection",
                "{0}/v1".format(uri),
                _create_json(name=name, description=description, locked=locked, servers=servers,
                             connection=connection), requires_modules=requires_modules,
                requires_version=requires_version)

    return isamAppliance.create_return_object()


def delete(isamAppliance, name=None, check_mode=False, force=False):
    """
    Deleting a Web Service connection
    """
    if force is True or _check_exists(isamAppliance, name=name) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            ret_obj = _get_id(isamAppliance, name=name)
            id = ret_obj['data']
            return isamAppliance.invoke_delete(
                "Deleting a Web Service connection",
                "{0}/{1}/v1".format(uri, id), requires_modules=requires_modules,
                requires_version=requires_version)

    return isamAppliance.create_return_object()


def update(isamAppliance, connection, description='', locked=False, servers=None, name=None,
           new_name=None, check_mode=False, force=False):
    """
    Modifying a Web Service connection

    Use new_name to rename the connection
    """
    if check_mode is True:
        return isamAppliance.create_return_object(changed=True)
    else:
        json_data = _create_json(name=name, description=description, locked=locked, servers=servers,
                                 connection=connection)
        if new_name is not None:  # Rename condition
            json_data['name'] = new_name
        return isamAppliance.invoke_put(
            "Modifying a Web Service connection",
            "{0}/{1}/v1".format(uri, id), json_data, requires_modules=requires_modules,
            requires_version=requires_version)


def _create_json(name, description, locked, servers, connection):
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
    # servers is optional
    if servers is not None:
        json['servers'] = servers

    return json


def _get_id(isamAppliance, name):
    """
    Retrieve UUID for named Web Service connection
    """
    ret_obj = get_all(isamAppliance)

    ret_obj_new = isamAppliance.create_return_object()

    for obj in ret_obj['data']:
        if obj['name'] == name:
            ret_obj_new['data'] = obj['uuid']

    return ret_obj_new


def _check_exists(isamAppliance, name=None, id=None):
    """
    Check if Web Service connection already exists
    """
    ret_obj = get_all(isamAppliance)

    for obj in ret_obj['data']:
        if (name is not None and obj['name'] == name) or (id is not None and obj['uuid'] == id):
            return True

    return False


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
