import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)

uri = "/snmpd/v1"


def get(isvgAppliance, check_mode=False, force=False):
    """
    Get SNMP Monitoring v1/2
    """
    return isvgAppliance.invoke_get("Get SNMP Monitoring Setup", uri)


def set_v1v2(isvgAppliance, community, port=161, check_mode=False, force=False):
    """
    Set SNMP Monitoring v1/2
    """
    if force is True or _checkv1_2(isvgAppliance, community, port) is False:
        if check_mode is True:
            return isvgAppliance.create_return_object(changed=True)
        else:
            return isvgAppliance.invoke_put(
                "Updating SNMP Monitoring", uri,
                {
                    "snmpv1v2c": {"community": community},
                    "enabled": True,
                    "port": port
                })

    return isvgAppliance.create_return_object()


def _checkv1_2(isvgAppliance, community, port):
    ret_obj = get(isvgAppliance)

    if ret_obj['data'][0]['enabled'] is False:
        logger.info("SNMP Monitoring is not enabled")
        return False

    if ret_obj['data'][0]['snmpv1v2c']['community'] != community:
        logger.info("SNMP Monitoring community is different")
        return False

    if ret_obj['data'][0]['port'] != port:
        logger.info("SNMP Monitoring port is different")
        return False

    return True


def set_v3(isvgAppliance, securityLevel, securityUser, authPassword, authProtocol, privacyPassword, privacyProtocol,
           port=161, check_mode=False, force=False):
    """
    Set SNMP Monitoring v3
    """
    if force is True or _checkV3(isvgAppliance, securityLevel, securityUser, authPassword, authProtocol,
                                 privacyPassword, privacyProtocol, port) is False:
        if check_mode is True:
            return isvgAppliance.create_return_object(changed=True)
        else:
            return isvgAppliance.invoke_put(
                "Updating SNMP Monitoring", uri,
                {
                    "snmpv3": {"securityLevel": securityLevel,
                               "securityUser": securityUser,
                               "authPassword": authPassword,
                               "authProtocol": authProtocol,
                               "privacyPassword": privacyPassword,
                               "privacyProtocol": privacyProtocol
                               },
                    "enabled": True,
                    "port": port
                })

    return isvgAppliance.create_return_object()


def _checkV3(isvgAppliance, securityLevel, securityUser, authPassword, authProtocol, privacyPassword, privacyProtocol,
             port):
    ret_obj = get(isvgAppliance)

    if ret_obj['data'][0]['enabled'] is False:
        logger.info("SNMP Monitoring is not enabled")
        return False

    if ret_obj['data'][0]['snmpv3']['securityLevel'] != securityLevel:
        logger.info("SNMP Monitoring security level is different")
        return False

    if ret_obj['data'][0]['snmpv3']['securityUser'] != securityUser:
        logger.info("SNMP Monitoring security user is different")
        return False

    if ret_obj['data'][0]['snmpv3']['authPassword'] != authPassword:
        logger.info("SNMP Monitoring auth password is different")
        return False

    if ret_obj['data'][0]['snmpv3']['authProtocol'] != authProtocol:
        logger.info("SNMP Monitoring auth protocol is different")
        return False

    if ret_obj['data'][0]['snmpv3']['privacyPassword'] != privacyPassword:
        logger.info("SNMP Monitoring privacy password is different")
        return False

    if ret_obj['data'][0]['snmpv3']['privacyProtocol'] != privacyProtocol:
        logger.info("SNMP Monitoring privacy protocol is different")
        return False

    if ret_obj['data'][0]['port'] != port:
        logger.info("SNMP Monitoring port is different")
        return False

    return True


def disable(isvgAppliance, check_mode=False, force=False):
    """
    Disable SNMP Monitoring
    """
    if force is False:
        ret_obj = get(isvgAppliance)

    if force is True or ret_obj['data'][0]['enabled'] is True:
        if check_mode is True:
            return isvgAppliance.create_return_object(changed=True)
        else:
            return isvgAppliance.invoke_put(
                "Disabling SNMP Monitoring", uri,
                {
                    "enabled": False
                })

    return isvgAppliance.create_return_object()


def compare(isvgAppliance1, isvgAppliance2):
    ret_obj1 = get(isvgAppliance1)
    ret_obj2 = get(isvgAppliance2)

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[])
