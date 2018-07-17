import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)


def get(isamAppliance, check_mode=False, force=False):
    """
    Retrieving the SNMP Monitoring configuration
    """
    return isamAppliance.invoke_get("Retrieving the SNMP Monitoring configuration", "/snmp/v1")


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


def set(isamAppliance, enabled, port=None, snmpv1v2c=None, snmpv3=None, check_mode=False, force=False):
    """
    Updating the SNMP Monitoring configuration
    """
    warnings = []
    if snmpv1v2c is not None and snmpv1v2c != '' and snmpv3 is not None and snmpv3 != '':
        warnings.append("SNMP v1v2 and v3 settings cannot be specified at the same time. Ignoring v1v2 settings.")
        snmpv1v2c = None
    update_required, json_data = _check_all(isamAppliance, snmpv1v2c, snmpv3, port, enabled)
    if force is True or update_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_put(
                "Updating the SNMP Monitoring configuration",
                "/snmp/v1", json_data, warnings=warnings)

    return isamAppliance.create_return_object(warnings=warnings)


def _check_all(isamAppliance, snmpv1v2c, snmpv3, port, enabled):
    json_data = {
        "enabled": enabled
    }
    if port is not None and port != '':
        json_data['port'] = port
    if snmpv1v2c is not None and snmpv1v2c != '':
        json_data['snmpv1v2c'] = snmpv1v2c
    if snmpv3 is not None and snmpv3 != '':
        json_data['snmpv3'] = snmpv3
    update_required = False

    ret_obj = get(isamAppliance)
    import ibmsecurity.utilities.tools
    sorted_json_data = ibmsecurity.utilities.tools.json_sort(json_data)
    logger.debug("Sorted input: {0}".format(sorted_json_data))
    sorted_ret_obj = ibmsecurity.utilities.tools.json_sort(ret_obj['data'])
    logger.debug("Sorted existing data: {0}".format(sorted_ret_obj))
    if sorted_ret_obj != sorted_json_data:
        logger.info("Changes detected, update needed.")
        update_required = True

    return update_required, json_data


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
