import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)


def get(isamAppliance, check_mode=False, force=False):
    """
    Get all snmp objects
    """
    return isamAppliance.invoke_get("Get all alert objects",
                                    "/core/system_alerts")


def enable(isamAppliance, uuid, objType, check_mode=False, force=False):
    """
    Enable a system alert
    """
    if force is True or _check(isamAppliance, uuid) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post(
                "Enable a system alert",
                "/core/system_alerts",
                {
                    'uuid': uuid,
                    'objType': objType
                })

    return isamAppliance.create_return_object()


def disable(isamAppliance, uuid, check_mode=False, force=False):
    """
    Delete a system alert
    """
    if force is True or _check(isamAppliance, uuid) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Delete a system alert",
                "/core/system_alerts/{0}".format(uuid))

    return isamAppliance.create_return_object()


def _check(isamAppliance, uuid):
    """
    Check if the system alert exists or not
    """
    ret_obj = get(isamAppliance)
    for obj in ret_obj['data']['responses']:
        if obj['uuid'] == uuid:
            return True

    return False


def compare(isamAppliance1, isamAppliance2):
    """
    Compare system alert objects between two appliances
    """
    ret_obj1 = get(isamAppliance1)
    ret_obj2 = get(isamAppliance2)

    for obj in ret_obj1['data']['responses']:
        del obj['uuid']
    for obj in ret_obj2['data']['responses']:
        del obj['uuid']

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=['uuid'])
