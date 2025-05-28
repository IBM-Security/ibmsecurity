import logging
import json

logger = logging.getLogger(__name__)

requires_modules = ["mga", "federation"]
requires_version = "10.0.8.0"

uri='/mga/server_connections/sms'

def get_all(isamAppliance, check_mode=False, force=False):
    """
    Retrieving a list of all SMS server connections
    """
    return isamAppliance.invoke_get("Retrieving a list of all SMS server connections",
                                    f"{uri}/v1",
                                    requires_modules=requires_modules, requires_version=requires_version)


def get(isamAppliance, name, check_mode=False, force=False):
    """
    Retrieving a SMS server connection
    """
    ret_obj = search(isamAppliance, name=name)
    id = ret_obj['data']

    if id == {}:
        return isamAppliance.create_return_object()
    else:
        return isamAppliance.invoke_get("Retrieving a SMS server connection",
                                        f"{uri}/{id}/v1",
                                        requires_modules=requires_modules, requires_version=requires_version)


def set(isamAppliance, name, connection, description='', locked=False, connectionManager=None, new_name=None, ignore_password_for_idempotency=False,
        check_mode=False, force=False):
    """
    Creating or Modifying an SMS server connection
    """
    if _check_exists(isamAppliance, name=name) is False:
        # Force the add - we already know connection does not exist
        return add(isamAppliance=isamAppliance, name=name, connection=connection, description=description,
                   locked=locked, connectionManager=connectionManager, check_mode=check_mode, force=True)
    else:
        # Update request
        return update(isamAppliance=isamAppliance, name=name, connection=connection, description=description,
                      locked=locked, connectionManager=connectionManager, new_name=new_name, ignore_password_for_idempotency=ignore_password_for_idempotency,
                      check_mode=check_mode, force=force)


def add(isamAppliance, name, connection, description='', locked=False, connectionManager=None, check_mode=False,
        force=False):
    """
    Creating a SMS server connection
    """
    if force is True or _check_exists(isamAppliance, name=name) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post(
                "Creating a SMS server connection",
                f"{uri}/v1",
                _create_json(name=name, description=description, locked=locked, connection=connection,
                             connectionManager=connectionManager),
                             requires_modules=requires_modules, requires_version=requires_version)

    return isamAppliance.create_return_object()


def delete(isamAppliance, name, check_mode=False, force=False):
    """
    Deleting a SMS server connection
    """
    if force is True or _check_exists(isamAppliance, name=name) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            ret_obj = search(isamAppliance, name=name)
            id = ret_obj['data']
            return isamAppliance.invoke_delete(
                "Deleting a SMS server connection",
                f"{uri}/{id}/v1",
                requires_modules=requires_modules, requires_version=requires_version)

    return isamAppliance.create_return_object()


def update(isamAppliance, name, connection, description='', locked=False, connectionManager=None, new_name=None, ignore_password_for_idempotency=False,
           check_mode=False, force=False):
    """
    Modifying a SMS server connection

    Use new_name to rename the connection.
    """
    ret_obj = get(isamAppliance, name)
    warnings = ret_obj["warnings"]

    if ret_obj["data"] == {}:
        warnings.append(f"SMS server connection {name} not found, skipping update.")
        return isamAppliance.create_return_object(warnings=warnings)
    else:
        id = ret_obj["data"]["uuid"]

    needs_update = False

    json_data = _create_json(name=name, description=description, locked=locked, connection=connection, connectionManager=connectionManager)
    if new_name is not None:  # Rename condition
        json_data['name'] = new_name
    if not force:
        ret_obj['data'].pop('uuid', None)
        if ignore_password_for_idempotency:
            if 'password' in connection:
                warnings.append("Request made to ignore password for idempotency check.")
                connection.pop('password', None)
        sorted_json_data = json.dumps(json_data, skipkeys=True, sort_keys=True)
        logger.debug(f"\n\nSorted input:         {sorted_json_data}")
        sorted_ret_obj = json.dumps(ret_obj['data'], skipkeys=True, sort_keys=True)
        logger.debug(f"\n\nSorted existing data: {sorted_ret_obj}")
        if sorted_ret_obj != sorted_json_data:
           needs_update = True
    if force or needs_update:
        if check_mode:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_put(
                "Modifying a SMS server connection",
                f"{uri}/{id}/v1",
                json_data,
                requires_modules=requires_modules, requires_version=requires_version, warnings=warnings)

def _create_json(name, description, locked, connection, connectionManager):
    """
    Create a JSON to be used for the REST API call
    """
    json = {
        "connection": connection,
        "type": "sms",
        "name": name,
        "description": description,
        "locked": locked
    }
    # connection manager is optional
    if connectionManager is not None:
        json['connectionManager'] = connectionManager

    return json


def search(isamAppliance, name, check_mode=False, force=False):
    """
    Retrieve UUID for named SMS connection
    """
    ret_obj = get_all(isamAppliance)

    ret_obj_new = isamAppliance.create_return_object()

    for obj in ret_obj['data']:
        if obj['name'] == name:
            ret_obj_new['data'] = obj['uuid']

    return ret_obj_new


def _check_exists(isamAppliance, name=None, id=None):
    """
    Check if SMS Connection already exists
    """
    ret_obj = get_all(isamAppliance)

    for obj in ret_obj['data']:
        if (name is not None and obj['name'] == name) or (id is not None and obj['uuid'] == id):
            return True

    return False


def compare(isamAppliance1, isamAppliance2):
    """
    Compare SMS Connections between two appliances
    """
    ret_obj1 = get_all(isamAppliance1)
    ret_obj2 = get_all(isamAppliance2)

    for obj in ret_obj1['data']:
        del obj['uuid']
    for obj in ret_obj2['data']:
        del obj['uuid']

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=['uuid'])
