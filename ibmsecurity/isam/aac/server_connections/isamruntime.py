import logging
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)
uri = "/mga/server_connections/isamruntime"
requires_modules = ["mga", "federation"]
requires_version = "9.0.5.0"


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Retrieving a list of all ISAM Runtime server connections
    """
    return isamAppliance.invoke_get("Retrieving a list of all ISAM Runtime server connections",
                                    "{0}/v1".format(uri),
                                    requires_modules=requires_modules, requires_version=requires_version)


def get(isamAppliance, name, check_mode=False, force=False):
    """
    Retrieving an ISAM Runtime server connection
    """

    ret_obj = search(isamAppliance, name=name)
    id = ret_obj['data']

    if id == {}:
        return isamAppliance.create_return_object()
    else:
        return isamAppliance.invoke_get("Retrieving an ISAM Runtime server connection",
                                        "{0}/{1}/v1".format(uri, id),
                                        requires_modules=requires_modules, requires_version=requires_version)


def add(isamAppliance, name, connection, description="", locked=False, check_mode=False, force=False):
    """
    Creating an ISAM Runtime server connection
    """

    if force is True or _check_exists(isamAppliance, name=name) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post(
                "Creating an ISAM Runtime server connection",
                "{0}/v1".format(uri),
                {
                    "locked": locked,
                    "description": description,
                    "type": "isamruntime",
                    "connection": connection,
                    "name": name
                },
                requires_modules=requires_modules, requires_version=requires_version
            )

    return isamAppliance.create_return_object()


def update(isamAppliance, name, connection, locked=False, description='', new_name=None, check_mode=False, force=False):
    """
    Modifying an ISAM Runtime server connection

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
                "Modifying an ISAM Runtime server connection",
                "{0}/{1}/v1".format(uri, id),
                json_data,
                requires_modules=requires_modules, requires_version=requires_version
            )

    return isamAppliance.create_return_object()


def set(isamAppliance, name, locked=False, connection=None, description=None, new_name=None,
        check_mode=False, force=False):
    """
    Creating or Modifying a isamruntime
    """
    ret_obj = search(isamAppliance, name=name)
    id = ret_obj['data']

    if id == {}:
        # If no uuid was found, Force the add
        return add(isamAppliance, name=name, locked=locked, connection=connection, description=description,
                   check_mode=check_mode, force=True)
    else:
        # Update isamruntime
        return update(isamAppliance, name=name, locked=locked, connection=connection, description=description,
                      new_name=new_name, check_mode=check_mode, force=force)


def delete(isamAppliance, name, check_mode=False, force=False):
    """
    Deleting an ISAM Runtime server connection

    """
    ret_obj = search(isamAppliance, name, check_mode=False, force=False)
    id = ret_obj['data']

    if force is True or id != {}:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:

            return isamAppliance.invoke_delete(
                "Deleting an ISAM Runtime server connection",
                "{0}/{1}/v1".format(uri, id),
                requires_modules=requires_modules, requires_version=requires_version
            )

    return isamAppliance.create_return_object()


def compare(isamAppliance1, isamAppliance2):
    """
    Compare isamruntime between two appliances
    """
    ret_obj1 = get_all(isamAppliance1)
    ret_obj2 = get_all(isamAppliance2)

    for obj in ret_obj1['data']:
        del obj['uuid']
    for obj in ret_obj2['data']:
        del obj['uuid']

    return tools.json_compare(ret_obj1, ret_obj2, deleted_keys=['uuid'])


def search(isamAppliance, name, force=False, check_mode=False):
    """
    Retrieve ID for isamruntime
    """
    ret_obj = get_all(isamAppliance)

    ret_obj_new = isamAppliance.create_return_object()

    for obj in ret_obj['data']:
        if obj['name'] == name:
            logger.info("Found isamruntime '{0}' uuid: '{1}'".format(name, obj['uuid']))
            ret_obj_new['data'] = obj['uuid']

    return ret_obj_new


def _check_exists(isamAppliance, name=None, id=None):
    """
    Check if ISAM runtime Connection already exists
    """
    ret_obj = get_all(isamAppliance)

    for obj in ret_obj['data']:
        if (name is not None and obj['name'] == name) or (id is not None and obj['uuid'] == id):
            return True

    return False


def _create_json(name, connection, description, locked):
    """
    Create a JSON to be used for the REST API call
    """
    json = {
        "connection": connection,
        "type": "isamruntime",
        "name": name,
        "description": description,
        "locked": locked
    }

    return json
