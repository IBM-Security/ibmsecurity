import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)

requires_model = "Appliance"

def get(isamAppliance, check_mode=False, force=False):
    """
    Retrieving the SNMP Monitoring configuration
    """
    return isamAppliance.invoke_get("Retrieving the SNMP Monitoring configuration", "/snmp/v1", requires_model=requires_model)


def set_v1v2(isamAppliance, community, port=161, check_mode=False, force=False):
    """
    Set SNMP Monitoring v1/2
    """
    snmpv1v2c = {
        "community": community
    }
    return set(isamAppliance, True, port, snmpv1v2c, None, check_mode, force)


def set_v3(isamAppliance, securityLevel, securityUser, authProtocol, authPassword, privacyProtocol, privacyPassword,
           port=161, check_mode=False, force=False):
    """
    Set SNMP Monitoring v3
    """
    snmpv3 = {
        "securityLevel": securityLevel,
        "securityUser": securityUser,
        "authProtocol": authProtocol,
        "authPassword": authPassword,
        "privacyProtocol": privacyProtocol,
        "privacyPassword": privacyPassword
    }
    return set(isamAppliance, True, port, None, snmpv3, check_mode, force)


def disable(isamAppliance, check_mode=False, force=False):
    """
    Disable SNMP Monitoring
    """
    return set(isamAppliance, False, None, None, None, check_mode, force)


def set(isamAppliance, enabled, port=None, snmpv1v2c=None, snmpv3=None, check_mode=False, force=False):
    """
    Updating the SNMP Monitoring configuration
    """
    warnings = []
    if snmpv1v2c is not None and snmpv1v2c != '' and snmpv3 is not None and snmpv3 != '':
        warnings.append("SNMP v1v2 and v3 settings cannot be specified at the same time. Ignoring v1v2 settings.")
        snmpv1v2c = None

    update_required, json_data, warn_str = _check_all(isamAppliance, snmpv1v2c, snmpv3, port, enabled)
    warnings = warnings + warn_str

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
    warnings = ret_obj['warnings']
    if warnings != []:
        if 'Docker' in warnings[0]:
            return update_required, json_data, warnings

    import ibmsecurity.utilities.tools
    sorted_json_data = ibmsecurity.utilities.tools.json_sort(json_data)
    logger.debug("Sorted input: {0}".format(sorted_json_data))
    sorted_ret_obj = ibmsecurity.utilities.tools.json_sort(ret_obj['data'])
    logger.debug("Sorted existing data: {0}".format(sorted_ret_obj))
    if sorted_ret_obj != sorted_json_data:
        logger.info("Changes detected, update needed.")
        update_required = True

    return update_required, json_data, warnings


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


def compare(isamAppliance1, isamAppliance2):
    ret_obj1 = get(isamAppliance1)
    ret_obj2 = get(isamAppliance2)

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[])
