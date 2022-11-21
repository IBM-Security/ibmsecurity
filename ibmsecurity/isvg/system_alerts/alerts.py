import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)


def get(isvgAppliance, check_mode=False, force=False):
    """
    Get all snmp objects
    """
    return isvgAppliance.invoke_get("Get all alert objects",
                                    "/system_alerts")


def enable(isvgAppliance, uuid, objType, check_mode=False, force=False):
    """
    Enable a system alert
    """
    if force is True or _check(isvgAppliance, uuid) is False:
        if check_mode is True:
            return isvgAppliance.create_return_object(changed=True)
        else:
            return isvgAppliance.invoke_post(
                "Enable a system alert",
                "/system_alerts",
                {
                    'uuid': uuid,
                    'objType': objType
                })

    return isvgAppliance.create_return_object()


def disable(isvgAppliance, uuid, check_mode=False, force=False):
    """
    Delete a system alert
    """
    if force is True or _check(isvgAppliance, uuid) is True:
        if check_mode is True:
            return isvgAppliance.create_return_object(changed=True)
        else:
            return isvgAppliance.invoke_delete(
                "Delete a system alert",
                "/system_alerts/{0}".format(uuid))

    return isvgAppliance.create_return_object()


def _check(isvgAppliance, uuid):
    """
    Check if the system alert exists or not
    """
    ret_obj = get(isvgAppliance)
    for obj in ret_obj['data']['responses']:
        if obj['uuid'] == uuid:
            return True

    return False


def compare(isvgAppliance1, isvgAppliance2):
    """
    Compare system alert objects between two appliances
    """
    ret_obj1 = get(isvgAppliance1)
    ret_obj2 = get(isvgAppliance2)

    for obj in ret_obj1['data']['responses']:
        del obj['uuid']
    for obj in ret_obj2['data']['responses']:
        del obj['uuid']

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=['uuid'])
