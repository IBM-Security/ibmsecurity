import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Get all logdb objects
    """
    return isamAppliance.invoke_get("Get all logdb objects",
                                    "/core/rsp_logdb_objs")


def get(isamAppliance, uuid, check_mode=False, force=False):
    """
    Get a specific logdb object
    """
    return isamAppliance.invoke_get("Get a specific logdb object",
                                    "/core/rsp_logdb_objs/{0}".format(uuid))


def add(isamAppliance, name, aclEventsAllocation, ipsEventsAllocation, sysEventsAllocation, objType='logdb',
        comment='', check_mode=False, force=False):
    """
    Add a logdb object

    NOTE: This function does not work!
    """
    if force is True or _check(isamAppliance, None, name, comment, aclEventsAllocation, ipsEventsAllocation,
                               sysEventsAllocation) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post(
                "Add a logdb object",
                "/core/rsp_logdb_objs/",
                {
                    'name': name,
                    'objType': objType,
                    'comment': comment,
                    'aclEventsAllocation': aclEventsAllocation,
                    'ipsEventsAllocation': ipsEventsAllocation,
                    'sysEventsAllocation': sysEventsAllocation
                })

    return isamAppliance.create_return_object()


def update(isamAppliance, name, uuid, aclEventsAllocation, ipsEventsAllocation, sysEventsAllocation, objType='logdb',
           comment='', check_mode=False, force=False):
    """
    Update a specific logdb object
    """
    if force is True or (
            _exists(isamAppliance, uuid) is True and _check(isamAppliance, uuid, name, comment, aclEventsAllocation,
                                                            ipsEventsAllocation, sysEventsAllocation) is False):
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Update a specific logdb object",
                "/core/rsp_logdb_objs/{0}".format(uuid),
                {
                    'name': name,
                    'uuid': uuid,
                    'objType': objType,
                    'comment': comment,
                    'aclEventsAllocation': aclEventsAllocation,
                    'ipsEventsAllocation': ipsEventsAllocation,
                    'sysEventsAllocation': sysEventsAllocation
                })

    return isamAppliance.create_return_object()


def delete(isamAppliance, uuid, check_mode=False, force=False):
    """
    Delete a logdb object

    NOTE: This function does not work!
    """
    if force is True or _exists(isamAppliance, uuid) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Delete a logdb object",
                "/core/rsp_logdb_objs/{0}".format(uuid))

    return isamAppliance.create_return_object()


def _exists(isamAppliance, uuid):
    """
    Check if an uuid object exists

    :param isamAppliance:
    :param uuid:
    :return:
    """
    exists = False
    ret_obj = get_all(isamAppliance)

    for snmp in ret_obj['data']['logdbObjects']:
        if snmp['uuid'] == uuid:
            exists = True
            break

    return exists


def _check(isamAppliance, uuid, name, comment, aclEventsAllocation, ipsEventsAllocation, sysEventsAllocation):
    """
    Check if the logdb object exists and is the same - uuid=None means add versus delete

    NOTE: if UUID is not found that will be same as no match!!!
    """
    set_value = {
        'name': name,
        'comment': comment,
        'objType': 'logdb',
        'uuid': uuid,
        'aclEventsAllocation': aclEventsAllocation,
        'ipsEventsAllocation': ipsEventsAllocation,
        'sysEventsAllocation': sysEventsAllocation
    }

    set_value = ibmsecurity.utilities.tools.json_sort(set_value)

    ret_obj = get_all(isamAppliance)
    for obj in ret_obj['data']['logdbObjects']:
        if uuid is None and obj['name'] == name:
            return True
        elif ibmsecurity.utilities.tools.json_sort(obj) == set_value:
            return True

    return False


def compare(isamAppliance1, isamAppliance2):
    """
    Compare logdb objects between two appliances
    """
    ret_obj1 = get_all(isamAppliance1)
    ret_obj2 = get_all(isamAppliance2)

    for obj in ret_obj1['data']['logdbObjects']:
        del obj['uuid']
    for obj in ret_obj2['data']['logdbObjects']:
        del obj['uuid']

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=['uuid'])
