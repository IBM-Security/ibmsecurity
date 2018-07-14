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


def set_v3(isamAppliance, securityLevel, securityUser, authProtocol, authPassword, privacyProtocol, privacyPassword, port=161, check_mode=False, force=False):
    """
    Set SNMP Monitoring v3
    """
    if force is True or _check_v3(isamAppliance, securityLevel, securityUser, authProtocol, authPassword, privacyProtocol, privacyPassword, port) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Updating SNMP Monitoring",
                "/snmp/v1",
                {
                    "snmpv3": {
                        "securityLevel": securityLevel,
                        "securityUser": securityUser,
                        "authProtocol": authProtocol,
                        "authPassword": authPassword,
                        "privacyProtocol": privacyProtocol,
                        "privacyPassword": privacyPassword
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

    if 'snmpv1v2c' in ret_obj['data']:
        logger.info("SNMP Monitoring snmpv1v2c object is present")
    else:
        logger.info("SNMP Monitoring snmpv1v2c object is missing")
        return False

    if ret_obj['data']['snmpv1v2c']['community'] != community:
        logger.info("SNMP Monitoring community is different")
        return False

    if ret_obj['data']['port'] != port:
        logger.info("SNMP Monitoring port is different")
        return False

    return True


def _check_v3(isamAppliance, securityLevel, securityUser, authProtocol, authPassword, privacyProtocol, privacyPassword, port):
    ret_obj = get(isamAppliance)

    if ret_obj['data']['enabled'] is False:
        logger.info("SNMP Monitoring is not enabled")
        return False

    if ret_obj['data']['port'] != port:
        logger.info("SNMP Monitoring port is different")
        return False

    if 'snmpv3' in ret_obj['data']:
        logger.info("SNMP Monitoring snmpv3 object is present")
    else:
        logger.info("SNMP Monitoring snmpv3 object is missing")
        return False

    if ret_obj['data']['snmpv3']['securityLevel'] != securityLevel:
        logger.info("SNMP Monitoring securityLevel is different")
        return False

    if ret_obj['data']['snmpv3']['securityUser'] != securityUser:
        logger.info("SNMP Monitoring securityUser is different")
        return False

    if ret_obj['data']['snmpv3']['authProtocol'] != authProtocol:
        logger.info("SNMP Monitoring authProtocol is different")
        return False

    if ret_obj['data']['snmpv3']['authPassword'] != authPassword:
        logger.info("SNMP Monitoring authPassword is different")
        return False

    if ret_obj['data']['snmpv3']['privacyProtocol'] != privacyProtocol:
        logger.info("SNMP Monitoring privacyProtocol is different")
        return False

    if ret_obj['data']['snmpv3']['privacyPassword'] != privacyPassword:
        logger.info("SNMP Monitoring privacyPassword is different")
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
