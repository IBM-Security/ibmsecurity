import logging
from ibmsecurity.utilities import tools
from ibmsecurity.appliance.ibmappliance import IBMError

logger = logging.getLogger(__name__)

requires_modules = ["mga", "federation"]
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
    ret_obj = _get_id(isamAppliance, name=name)
    id = ret_obj['data']

    if id == {}:
        return isamAppliance.create_return_object(1)
    else:
        return isamAppliance.invoke_get("Retrieving a CI server connection",
                                        "/mga/server_connections/ci/{0}/v1".format(id),
                                        requires_modules=requires_modules, requires_version=requires_version)


def set(isamAppliance, name, connection, description='', locked=False, check_mode=False, force=False):
    """
    Creating or Modifying a CI server connection
    """
    if _check_exists(isamAppliance, name=name) is False:
        # Force the add - we already know connection does not exist
        return add(isamAppliance, name=name, connection=connection, description=description, locked=locked, check_mode=check_mode, force=True)
    else:
        # Update request
        return update(isamAppliance, connection=connection, description=description, locked=locked, name=name, check_mode=check_mode, force=force)


def add(isamAppliance, name, connection, description='', locked=False, check_mode=False, force=False):
    """
    Creating a CI server connection
    """

    response = isamAppliance.create_return_object();

    if force is True or _check_exists(isamAppliance, name=name) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            try:
                response = isamAppliance.invoke_post(
                    "Creating a CI server connection",
                    "/mga/server_connections/ci/v1",
                    _create_json(name=name, description=description, locked=locked, connection=connection),
                    requires_modules=requires_modules, requires_version=requires_version)


            except IBMError as e:
                if "400" in e[0]:
                    response = isamAppliance.create_return_object(rc=400, data=e[1]);
                elif "409" in e[0]:
                    response = isamAppliance.create_return_object(rc=409, data=e[1]);
                else:
                    raise;

    return response;


def delete(isamAppliance, name=None, id=None, check_mode=False, force=False):
    """
    Deleting a CI server connection
    """
    if force is True or _check_exists(isamAppliance, name=name, id=id) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            if id is None:
                ret_obj = _get_id(isamAppliance, name=name)
                id = ret_obj['data']
            try:
                response = isamAppliance.invoke_delete(
                    "Deleting a CI server connection",
                    "/mga/server_connections/ci/{0}/v1".format(id), requires_modules=requires_modules,
                    requires_version=requires_version)
            except IBMError as e:
                if "404" in e[0]:
                    response = isamAppliance.create_return_object(rc=404, data=e[1]);
                else:
                    raise;

    return response;


def update(isamAppliance, name, connection, description='', locked=False, new_name=None, check_mode=False, force=False, ):
    """
    Modifying a CI server connection
    Use new_name to rename the connection.
    """
    ret_obj = get(isamAppliance, name)
    warnings = ret_obj["warnings"]

    if ret_obj["data"] == {}:
        warnings.append("CI Service connection {0} not found, skipping update.".format(name))
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
        if 'clientSecret' in connection:
            warnings.append("Since existing clientSecret cannot be read - this parameter will be ignored for idempotency. Add 'force' parameter to update the connection with a new clientSecret.")
            connection.pop('clientSecret', None)

        sorted_ret_obj = tools.json_sort(ret_obj['data'])
        sorted_json_data = tools.json_sort(json_data)
        logger.debug("Sorted Existing Data:{0}".format(sorted_ret_obj))
        logger.debug("Sorted Desired  Data:{0}".format(sorted_json_data))

        if sorted_ret_obj != sorted_json_data:
            needs_update = True
    
    if force is True or needs_update is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            try:
              response = isamAppliance.invoke_put(
                  "Modifying a CI server connection",
                  "/mga/server_connections/ci/{0}/v1".format(id), json_data, requires_modules=requires_modules,
                  requires_version=requires_version)
            except IBMError as e:
                if "400" in e[0]:
                    response = isamAppliance.create_return_object(rc=400, data=e[1]);
                else:
                    raise;

            return response;

    return isamAppliance.create_return_object(warnings=warnings)

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


def _get_id(isamAppliance, name):
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
