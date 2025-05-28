import logging
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

requires_modules = ["mga", "federation"]
requires_version = None

def get_all(isamAppliance, check_mode=False, force=False):
    """
    Retrieving a list of all LDAP server connections
    """
    return isamAppliance.invoke_get("Retrieving a list of all LDAP server connections",
                                    "/mga/server_connections/ldap/v1",
                                    requires_modules=requires_modules, requires_version=requires_version)


def get(isamAppliance, name, check_mode=False, force=False):
    """
    Retrieving an LDAP server connection
    """
    ret_obj = search(isamAppliance, name=name)
    id = ret_obj['data']

    if id == {}:
        return isamAppliance.create_return_object()
    else:
        return isamAppliance.invoke_get("Retrieving an LDAP server connection",
                                        f"/mga/server_connections/ldap/{id}/v1",
                                        requires_modules=requires_modules, requires_version=requires_version)


def set(isamAppliance, name, connection, description='', locked=False, connectionManager=None, servers=None,
        new_name=None, ignore_password_for_idempotency=False, check_mode=False, force=False):
    """
    Creating or Modifying an LDAP server connection
    """
    if _check_exists(isamAppliance, name=name) is False:
        # Force the add - we already know connection does not exist
        return add(isamAppliance=isamAppliance, name=name, connection=connection, description=description,
                   locked=locked, connectionManager=connectionManager, servers=servers, check_mode=check_mode,
                   force=True)
    else:
        # Update request
        return update(isamAppliance=isamAppliance, name=name, connection=connection, description=description,
                      locked=locked, connectionManager=connectionManager, servers=servers, new_name=new_name, ignore_password_for_idempotency=ignore_password_for_idempotency,
                      check_mode=check_mode, force=force)


def add(isamAppliance, name, connection, description='', locked=False, connectionManager=None, servers=None,
        check_mode=False, force=False):
    """
    Creating an LDAP server connection
    """
    if force is True or _check_exists(isamAppliance, name=name) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post(
                "Creating an LDAP server connection",
                "/mga/server_connections/ldap/v1",
                _create_json(name=name, description=description, locked=locked, servers=servers,
                             connection=connection, connectionManager=connectionManager),
                requires_modules=requires_modules, requires_version=requires_version)

    return isamAppliance.create_return_object()


def delete(isamAppliance, name, check_mode=False, force=False):
    """
    Deleting an LDAP server connection
    """
    if force is True or _check_exists(isamAppliance, name=name) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            ret_obj = search(isamAppliance, name=name)
            id = ret_obj['data']
            return isamAppliance.invoke_delete(
                "Deleting an LDAP server connection",
                f"/mga/server_connections/ldap/{id}/v1",
                requires_modules=requires_modules, requires_version=requires_version)

    return isamAppliance.create_return_object()


def update(isamAppliance, name, connection, description='', locked=False, connectionManager=None, servers=None,
           new_name=None, ignore_password_for_idempotency=False, check_mode=False, force=False):
    """
    Modifying an LDAP server connection

    Use new_name to rename the connection.
    """
    ret_obj = get(isamAppliance, name)
    warnings = ret_obj["warnings"]

    if ret_obj["data"] == {}:
        warnings.append(f"LDAP server connection {name} not found, skipping update.")
        return isamAppliance.create_return_object(warnings=warnings)
    else:
        id = ret_obj["data"]["uuid"]

    needs_update = False

    json_data = _create_json(name=name, description=description, locked=locked, servers=servers, connection=connection, connectionManager=connectionManager)
    if new_name is not None:  # Rename condition
        json_data['name'] = new_name

    if force is not True:
        if 'uuid' in ret_obj['data']:
            del ret_obj['data']['uuid']
        if ignore_password_for_idempotency:
            if 'bindPwd' in connection:
                warnings.append("Request made to ignore bindPwd for idempotency check.")
                connection.pop('bindPwd', None)

        sorted_ret_obj = tools.json_sort(ret_obj['data'])
        sorted_json_data = tools.json_sort(json_data)
        logger.debug(f"Sorted Existing Data:{sorted_ret_obj}")
        logger.debug(f"Sorted Desired  Data:{sorted_json_data}")

        if sorted_ret_obj != sorted_json_data:
            needs_update = True

    if force is True or needs_update is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_put(
                "Modifying an LDAP server connection",
                f"/mga/server_connections/ldap/{id}/v1", json_data,
                requires_modules=requires_modules, requires_version=requires_version, warnings=warnings)

    return isamAppliance.create_return_object(warnings=warnings)

def _create_json(name, description, locked, servers, connection, connectionManager):
    """
    Create a JSON to be used for the REST API call
    """
    json = {
        "connection": connection,
        "type": "ldap",
        "name": name,
        "description": description,
        "locked": locked
    }
    # connection manager and servers is optional
    if connectionManager is not None:
        json['connectionManager'] = connectionManager
    if servers is not None:
        json['servers'] = servers

    return json


def search(isamAppliance, name):
    """
    Retrieve UUID for named LDAP connection
    """
    ret_obj = get_all(isamAppliance)

    ret_obj_new = isamAppliance.create_return_object()

    for obj in ret_obj['data']:
        if obj['name'] == name:
            ret_obj_new['data'] = obj['uuid']

    return ret_obj_new


def _check_exists(isamAppliance, name=None, id=None):
    """
    Check if LDAP Connection already exists
    """
    ret_obj = get_all(isamAppliance)

    for obj in ret_obj['data']:
        if (name is not None and obj['name'] == name) or (id is not None and obj['uuid'] == id):
            return True

    return False


def compare(isamAppliance1, isamAppliance2):
    """
    Compare LDAP Connections between two appliances
    """
    ret_obj1 = get_all(isamAppliance1)
    ret_obj2 = get_all(isamAppliance2)

    for obj in ret_obj1['data']:
        del obj['uuid']
    for obj in ret_obj2['data']:
        del obj['uuid']

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=['uuid'])
