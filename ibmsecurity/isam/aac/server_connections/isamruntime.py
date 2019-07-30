import logging

from ibmsecurity.utilities import tools
from ibmsecurity.utilities.tools import json_sort

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


def get(isamAppliance, name=None, check_mode=False, force=False):
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


def add(isamAppliance, name, connection, description="", locked=False, type="isamruntime", check_mode=False,
        force=False):
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


def update(isamAppliance, name, connection, locked=False, description=None, type="isamruntime", new_name=None,
           check_mode=False, force=False):
    """
    Modifying an ISAM Runtime server connection

    """

    ret_obj = search(isamAppliance, name=name)
    uuid = ret_obj['data']

    update_required = False

    if uuid != {}:
        ret_obj = get(isamAppliance, uuid)

        json_data = {
            "locked": locked,
            "uuid": uuid,
            "description": description,
            "type": "isamruntime",
            "connection": connection
        }

        del json_data['connection']['bindPwd']

        if new_name != None:
            json_data['name'] = new_name
        else:
            json_data['name'] = name

        sorted_json_data = json_sort(json_data)

        logger.debug("Sorted input: {0}".format(sorted_json_data))

        sorted_ret_obj = json_sort(ret_obj['data'])

        logger.debug("Sorted existing data: {0}".format(sorted_ret_obj))

        if sorted_json_data != sorted_ret_obj:
            update_required = True
            json_data['connection'] = connection
    else:
        logger.info("isamruntime '{0}' does not exists.  Skipping update.".format(name))
        warnings = ["isamruntime '{0}' does not exists.  Skipping update.".format(name)]
        return isamAppliance.create_return_object(warnings=warnings)

    if force is True or update_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:

            return isamAppliance.invoke_put(
                "Modifying an ISAM Runtime server connection",
                "{0}/{1}/v1".format(uri, uuid),
                json_data,
                requires_modules=requires_modules, requires_version=requires_version
            )

    if update_required is False:
        logger.info("Input is the same as current isamruntime '{0}'.  Skipping update.".format(name))

    return isamAppliance.create_return_object()


def set(isamAppliance, name, locked=False, connection=None, description=None, type="isamruntime", new_name=None,
        check_mode=False, force=False):
    """
    Creating or Modifying a isamruntime
    """
    ret_obj = search(isamAppliance, name=name)
    uuid = ret_obj['data']

    if uuid == {}:
        # If no uuid was found, Force the add
        return add(isamAppliance, name=name, locked=locked, connection=connection, description=description,
                   check_mode=check_mode, force=True)
    else:
        # Update isamruntime
        return update(isamAppliance, name=name, locked=locked, connection=connection, description=description,
                      new_name=new_name, check_mode=check_mode, force=force)


def delete(isamAppliance, name=None, check_mode=False, force=False):
    """
    Deleting an ISAM Runtime server connection

    """
    ret_obj = search(isamAppliance, name, check_mode=False, force=False)
    uuid = ret_obj['data']

    if force is True or uuid != {}:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:

            return isamAppliance.invoke_delete(
                "Deleting an ISAM Runtime server connection",
                "{0}/{1}/v1".format(uri, uuid),
                requires_modules=requires_modules, requires_version=requires_version
            )

    if uuid == {}:
        logger.info("PIP '{0}' does not exists, skipping delete.".format(name))

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
