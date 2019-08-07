import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)

requires_modules = ["mga"]
requires_version = "9.0.5.0"


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Retrieving a list of all CI server connections
    """
    return isamAppliance.invoke_get("Retrieving a list of all CI server connections",
                                    "/mga/server_connections/ci/v1", requires_modules=requires_modules,
                                    requires_version=requires_version)


def get(isamAppliance, name, check_mode=False, force=False):
    """
    Retrieving a CI server connection
    """
    ret_obj = search(isamAppliance, name=name)
    id = ret_obj['data']

    if id == {}:
        return isamAppliance.create_return_object()
    else:
        return isamAppliance.invoke_get("Retrieving a CI server connection",
                                        "/mga/server_connections/ci/{0}/v1".format(id),
                                        requires_modules=requires_modules, requires_version=requires_version)


def set(isamAppliance, name, connection, description='', locked=False, new_name=None, check_mode=False, force=False):
    """
    Creating or Modifying a CI server connection
    """
    if _check_exists(isamAppliance, name=name) is False:
        # Force the add - we already know connection does not exist
        return add(isamAppliance=isamAppliance, name=name, connection=connection, description=description,
                   locked=locked, check_mode=check_mode, force=True)
    else:
        # Update request
        return update(isamAppliance=isamAppliance, name=name, connection=connection, description=description,
                      locked=locked, new_name=new_name, check_mode=check_mode, force=force)


def add(isamAppliance, name, connection, description='', locked=False, check_mode=False, force=False):
    """
    Creating a CI server connection
    """

    if force is True or _check_exists(isamAppliance, name=name) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post(
                "Creating a CI server connection",
                "/mga/server_connections/ci/v1",
                _create_json(name=name, description=description, locked=locked, connection=connection),
                requires_modules=requires_modules, requires_version=requires_version)

    return isamAppliance.create_return_object()


def delete(isamAppliance, name, check_mode=False, force=False):
    """
    Deleting a CI server connection
    """
    if force is True or _check_exists(isamAppliance, name=name) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            ret_obj = search(isamAppliance, name=name)
            id = ret_obj['data']
            return isamAppliance.invoke_delete(
                "Deleting a CI server connection",
                "/mga/server_connections/ci/{0}/v1".format(id), requires_modules=requires_modules,
                requires_version=requires_version)

    return isamAppliance.create_return_object()


def update(isamAppliance, name, connection, description='', locked=False, new_name=None, check_mode=False, force=False):
    """
    Modifying a CI server connection
    Use new_name to rename the connection, cannot compare password so update will take place everytime
    """

    if force is True or _check_exists(isamAppliance, name):
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            json_data = _create_json(name=name, description=description, locked=locked, connection=connection)
            if new_name is not None:  # Rename condition
                json_data['name'] = new_name
            ret_obj = search(isamAppliance, name=name)
            id = ret_obj['data']
            return isamAppliance.invoke_put(
                "Modifying a CI server connection",
                "/mga/server_connections/ci/{0}/v1".format(id), json_data, requires_modules=requires_modules,
                requires_version=requires_version)

    return isamAppliance.create_return_object()


def _create_json(name, description, locked, connection):
    """
    Create a JSON to be used for the REST API call
    """
    json = {
        "connection": connection,
        "type": "ci",
        "name": name,
        "description": description,
        "locked": locked
    }

    return json


def search(isamAppliance, name):
    """
    Retrieve UUID for named CI connection
    """
    ret_obj = get_all(isamAppliance)

    ret_obj_new = isamAppliance.create_return_object()

    for obj in ret_obj['data']:
        if obj['name'] == name:
            ret_obj_new['data'] = obj['uuid']

    return ret_obj_new


def _check_exists(isamAppliance, name=None, id=None):
    """
    Check if CI Connection already exists
    """
    ret_obj = get_all(isamAppliance)

    for obj in ret_obj['data']:
        if (name is not None and obj['name'] == name) or (id is not None and obj['uuid'] == id):
            return True

    return False


def compare(isamAppliance1, isamAppliance2):
    """
    Compare CI Connections between two appliances
    """
    ret_obj1 = get_all(isamAppliance1)
    ret_obj2 = get_all(isamAppliance2)

    for obj in ret_obj1['data']:
        del obj['uuid']
    for obj in ret_obj2['data']:
        del obj['uuid']

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=['uuid'])
