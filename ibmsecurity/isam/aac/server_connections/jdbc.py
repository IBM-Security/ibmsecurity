import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Retrieving a list of all JDBC server connections
    """
    return isamAppliance.invoke_get("Retrieving a list of all JDBC server connections",
                                    "/mga/server_connections/jdbc/v1")


def get(isamAppliance, name, check_mode=False, force=False):
    """
    Retrieving a JDBC server connection
    """
    ret_obj = search(isamAppliance, name=name)
    id = ret_obj['data']

    if id == {}:
        return isamAppliance.create_return_object()
    else:
        return isamAppliance.invoke_get("Retrieving a JDBC server connection",
                                        "/mga/server_connections/jdbc/{0}/v1".format(id))


def set(isamAppliance, name, connection, type, jndiId, description='', locked=False, connectionManager=None,
        new_name=None, check_mode=False, force=False):
    """
    Creating or Modifying an JDBC server connection
    """
    if _check_exists(isamAppliance, name=name) is False:
        # Force the add - we already know connection does not exist
        return add(isamAppliance, name=name, connection=connection, type=type, jndiId=jndiId, description=description,
                   locked=locked, connectionManager=connectionManager, check_mode=check_mode,
                   force=True)
    else:
        # Update request
        return update(isamAppliance=isamAppliance, name=name, connection=connection, type=type, jndiId=jndiId,
                      description=description, locked=locked, connectionManager=connectionManager, new_name=new_name,
                      check_mode=check_mode, force=force)


def add(isamAppliance, name, connection, type, jndiId, description='', locked=False, connectionManager=None,
        check_mode=False, force=False):
    """
    Creating a JDBC server connection
    """
    if force is True or _check_exists(isamAppliance, name=name) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post(
                "Creating a JDBC server connection",
                "/mga/server_connections/jdbc/v1",
                _create_json(name=name, description=description, locked=locked, type=type, connection=connection,
                             connectionManager=connectionManager, jndiId=jndiId))

    return isamAppliance.create_return_object()


def delete(isamAppliance, name, check_mode=False, force=False):
    """
    Deleting a JDBC server connection
    """
    if force is True or _check_exists(isamAppliance, name=name) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            ret_obj = search(isamAppliance, name=name)
            id = ret_obj['data']
            return isamAppliance.invoke_delete(
                "Deleting a JDBC server connection",
                "/mga/server_connections/jdbc/{0}/v1".format(id))

    return isamAppliance.create_return_object()


def update(isamAppliance, name, connection, type, jndiId, description='', locked=False, connectionManager=None,
           new_name=None, check_mode=False, force=False):
    """
    Modifying a JDBC server connection

    Use new_name to rename the connection, cannot compare password so update will take place everytime
    """

    if force is True or _check_exists(isamAppliance, name):
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            json_data = _create_json(name=name, description=description, locked=locked, type=type,
                                     connection=connection, connectionManager=connectionManager, jndiId=jndiId)
            ret_obj = search(isamAppliance, name)
            id = ret_obj['data']

            if new_name is not None:  # Rename condition
                json_data['name'] = new_name

            return isamAppliance.invoke_put("Modifying a JDBC server connection",
                                            "/mga/server_connections/jdbc/{0}/v1".format(id), json_data)

    return isamAppliance.create_return_object()


def _create_json(name, description, locked, type, jndiId, connection, connectionManager):
    """
    Create a JSON to be used for the REST API call
    """
    json = {
        "connection": connection,
        "type": type,
        "jndiId": jndiId,
        "name": name,
        "description": description,
        "locked": locked
    }
    # connection manager is optional
    if connectionManager is not None:
        json['connectionManager'] = connectionManager

    return json


def search(isamAppliance, name):
    """
    Retrieve UUID for named JDBC connection
    """
    ret_obj = get_all(isamAppliance)

    ret_obj_new = isamAppliance.create_return_object()

    for obj in ret_obj['data']:
        if obj['name'] == name:
            ret_obj_new['data'] = obj['uuid']

    return ret_obj_new


def _check_exists(isamAppliance, name=None, id=None):
    """
    Check if JDBC Connection already exists
    """
    ret_obj = get_all(isamAppliance)

    for obj in ret_obj['data']:
        if (name is not None and obj['name'] == name) or (id is not None and obj['uuid'] == id):
            return True

    return False


def compare(isamAppliance1, isamAppliance2):
    """
    Compare JDBC Connections between two appliances
    """
    ret_obj1 = get_all(isamAppliance1)
    ret_obj2 = get_all(isamAppliance2)

    for obj in ret_obj1['data']:
        del obj['uuid']
    for obj in ret_obj2['data']:
        del obj['uuid']

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=['uuid'])
