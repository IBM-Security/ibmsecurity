import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)


def get(isamAppliance, check_mode=False, force=False):
    """
    Get SNMP Monitoring v1/2
    """
    return isamAppliance.invoke_get("Get SNMP Monitoring Setup",
                                    "/snmp/v1")


def set_v1v2(isamAppliance, community, port=161, check_mode=False, force=False):
    """
    Set SNMP Monitoring v1/2
    """
    if force is True or _check(isamAppliance, community, port) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Updating SNMP Monitoring",
                "/snmp/v1",
                {
                    "snmpv1v2c": {
                        "community": community
                    },
                    "enabled": True,
                    "port": port
                })

    return isamAppliance.create_return_object()


def _check(isamAppliance, community, port):
    ret_obj = get(isamAppliance)

    if ret_obj['data']['enabled'] is False:
        logger.info("SNMP Monitoring is not enabled")
        return False

    if ret_obj['data']['snmpv1v2c']['community'] != community:
        logger.info("SNMP Monitoring community is different")
        return False

    if ret_obj['data']['port'] != port:
        logger.info("SNMP Monitoring port is different")
        return False

    return True


def disable(isamAppliance, check_mode=False, force=False):
    """
    Disable SNMP Monitoring
    """
    if force is False:
        ret_obj = get(isamAppliance)

    if force is True or ret_obj['data'][0]['enabled'] is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Disabling SNMP Monitoring",
                "/snmp/v1",
                {
                    "enabled": False
                })

    return isamAppliance.create_return_object()


def compare(isamAppliance1, isamAppliance2):
    ret_obj1 = get(isamAppliance1)
    ret_obj2 = get(isamAppliance2)

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[])
