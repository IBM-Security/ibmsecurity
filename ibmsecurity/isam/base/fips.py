import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)


def get(isamAppliance, check_mode=False, force=False):
    """
    Get SNMP Monitoring v1/2
    """
    return isamAppliance.invoke_get("Get FIPS Settings",
                                    "/fips_cfg")


def set(isamAppliance, fipsEnabled=True, tlsv10Enabled=True, tlsv11Enabled=False, check_mode=False, force=False):
    """
    Set FIPS mode
    """
    if force is True or _check(isamAppliance, fipsEnabled, tlsv10Enabled, tlsv11Enabled) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Set FIPS Mode",
                "/fips_cfg",
                {
                    "fipsEnabled": fipsEnabled,
                    "tlsv10Enabled": tlsv10Enabled,
                    "tlsv11Enabled": tlsv11Enabled
                })

    return isamAppliance.create_return_object()


def restart(isamAppliance, check_mode=False, force=False):
    """
    Restart after FIPS configuration changes
    :param isamAppliance:
    :param check_mode:
    :param force:
    :return:
    """
    if check_mode is True:
        return isamAppliance.create_return_object(changed=True)
    else:
        return isamAppliance.invoke_put(
            "Restart after FIPS configuration change",
            "/fips_cfg/restart",
            {}
        )


def _check(isamAppliance, fipsEnabled, tlsv10Enabled, tlsv11Enabled):
    ret_obj = get(isamAppliance)

    if ret_obj['data']['fipsEnabled'] != fipsEnabled:
        logger.info("fipsEnabled change to {0}".format(fipsEnabled))
        return False

    if ret_obj['data']['tlsv10Enabled'] != tlsv10Enabled:
        logger.info("TLS v1.0 change to {0}".format(tlsv10Enabled))
        return False

    if ret_obj['data']['tlsv11Enabled'] != tlsv11Enabled:
        logger.info("TLS v1.1 change to {0}".format(tlsv11Enabled))
        return False

    return True


def compare(isamAppliance1, isamAppliance2):
    ret_obj1 = get(isamAppliance1)
    ret_obj2 = get(isamAppliance2)

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[])
